#!/usr/bin/env python3
"""
Créer un nouveau chat Diplomeo dev avec le prompt corrigé
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

# Configuration du nouveau chat
payload = {
    "name": "Diplomeo dev v2",
    "description": "A helpful Assistant (avec prompt corrigé)",
    "language": "English",
    "prompt_type": "simple",
    "do_refer": "1",
    "top_k": 20,
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
        "rerank_model": "BAAI/bge-reranker-v2-m3",
        "empty_response": "",
        "opener": "# Salut ! Je suis ton conseiller d'orientation. 👋\n\n### **Regarde ce que je peux faire pour toi :**\n\n* **🔍 Explore un métier**\n    Recherche un métier pour découvrir les missions réelles et les débouchés.\n* **🗺️ Trace ton parcours**\n    Découvre quel diplôme viser, du **CAP au Master**, selon ton profil actuel.\n* **🏫 Trouve ton école ou ton centre de formation**\n    Identifie les établissements disponibles dans ta région.\n* **🤰 Adapte ta formation**\n    Parle-moi de tes contraintes (grossesse, job actuel, vie de famille) pour trouver un rythme flexible.\n\n---\n\n**Dis-moi, dans quelle direction veux-tu orienter ton avenir aujourd'hui ?**",
        "prompt": prompt_text
    }
}

print("🚀 Création du nouveau chat 'Diplomeo dev v2'...")
print(f"Prompt: {len(prompt_text)} caractères")

url = f"{RAGFLOW_HOST}/api/v1/chats"
response = requests.post(url, headers=HEADERS, json=payload)

print(f"\nStatus code: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    data = response.json()
    if data.get('code') == 0:
        new_chat = data.get('data', {})
        new_chat_id = new_chat.get('id')
        print(f"\n✅ Chat créé avec succès!")
        print(f"Nom: {new_chat.get('name')}")
        print(f"ID: {new_chat_id}")
        
        # Sauvegarder le nouveau chat ID
        with open('new_chat_dev_id.txt', 'w') as f:
            f.write(new_chat_id)
        
        print(f"\n💾 ID sauvegardé dans: new_chat_dev_id.txt")
        print("\n✅ Vous pouvez maintenant lancer les tests avec ce nouveau chat!")
    else:
        print(f"❌ Erreur: {data.get('message')}")
else:
    print(f"❌ Erreur HTTP: {response.status_code}")
