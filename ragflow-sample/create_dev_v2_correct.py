#!/usr/bin/env python3
"""
Créer Diplomeo dev v2 avec TOUS les bons paramètres (incluant Top-K reranking)
"""

import requests
import json

RAGFLOW_HOST = "https://rag-staging.flowkura.com"
API_KEY = "ragflow-d4iWypSjduSHlkWb-wFOwda57ytZFsE7sxc6npOt9b8"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Lire le prompt
with open('prompt_from_prod.txt', 'r', encoding='utf-8') as f:
    prompt_text = f.read()

# Configuration COMPLÈTE du chat (copie exacte de Diplomeo prod)
payload = {
    "name": "Diplomeo dev v2",
    "description": "A helpful Assistant (avec prompt corrigé)",
    "language": "English",
    "prompt_type": "simple",
    "do_refer": "1",
    "top_k": 2048,  # ← CORRIGÉ: Top-K du RERANKING (pas du LLM)
    "llm": {
        "model_name": "Qwen/Qwen3___VLLM@VLLM",
        "temperature": 0.7,
        "top_p": 0.8,
        "presence_penalty": 0.5,
        "frequency_penalty": 0.5
    },
    "dataset_ids": [
        "dc762171fb2811f0a03402420a000115",  # Métiers
        "e1c6982ffb2811f0a05d02420a000115",  # Formations
        "e8ad1a3afb2811f09a1f02420a000115",  # Actions de Formation
        "29b4d83bfb2911f0bbfa02420a000115"   # Établissements
    ],
    "prompt": {
        "similarity_threshold": 0.2,
        "keywords_similarity_weight": 0.3,
        "top_n": 8,
        "variables": [{"key": "knowledge", "optional": False}],
        "rerank_model": "BAAI/bge-reranker-v2-m3",  # ← CRITIQUE
        "empty_response": "",
        "show_quote": False,
        "tts": False,
        "refine_multiturn": False,
        "opener": "# Salut ! Je suis ton conseiller d'orientation. 👋\n\n### **Regarde ce que je peux faire pour toi :**\n\n* **🔍 Explore un métier**\n    Recherche un métier pour découvrir les missions réelles et les débouchés.\n* **🗺️ Trace ton parcours**\n    Découvre quel diplôme viser, du **CAP au Master**, selon ton profil actuel.\n* **🏫 Trouve ton école ou ton centre de formation**\n    Identifie les établissements disponibles dans ta région.\n* **🤰 Adapte ta formation**\n    Parle-moi de tes contraintes (grossesse, job actuel, vie de famille) pour trouver un rythme flexible.\n\n---\n\n**Dis-moi, dans quelle direction veux-tu orienter ton avenir aujourd'hui ?**",
        "prompt": prompt_text
    }
}

print("🚀 Création de 'Diplomeo dev v2' avec TOUS les bons paramètres...")
print(f"   - Top-K reranking: 2048")
print(f"   - Rerank model: BAAI/bge-reranker-v2-m3")
print(f"   - Temperature: 0.7")
print(f"   - Top P: 0.8")
print(f"   - Prompt: {len(prompt_text)} caractères\n")

url = f"{RAGFLOW_HOST}/api/v1/chats"
response = requests.post(url, headers=HEADERS, json=payload)

print(f"Status code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    if data.get('code') == 0:
        new_chat = data.get('data', {})
        new_chat_id = new_chat.get('id')
        
        print(f"\n✅ Chat créé avec succès!")
        print(f"   Nom: {new_chat.get('name')}")
        print(f"   ID: {new_chat_id}")
        print(f"   Top-K: {new_chat.get('top_k')}")
        
        # Vérifier le rerank model
        rerank = new_chat.get('prompt', {}).get('rerank_model')
        print(f"   Rerank model: {rerank}")
        
        # Sauvegarder
        with open('new_chat_dev_id.txt', 'w') as f:
            f.write(new_chat_id)
        
        print(f"\n💾 ID sauvegardé dans: new_chat_dev_id.txt")
        
        # Vérifier la RÈGLE CRITIQUE
        print("\n🔍 Vérification du prompt...")
        if "RÈGLE CRITIQUE" in new_chat.get('prompt', {}).get('prompt', ''):
            print("   ✅ RÈGLE CRITIQUE présente")
        else:
            print("   ❌ RÈGLE CRITIQUE manquante!")
        
        print("\n✅ Tout est prêt! Vous pouvez lancer les tests.")
    else:
        print(f"❌ Erreur: {data.get('message')}")
        print(f"\nRéponse complète:\n{json.dumps(data, indent=2)}")
else:
    print(f"❌ Erreur HTTP: {response.status_code}")
    print(f"Réponse: {response.text}")
