#!/usr/bin/env python3
"""
Copier le prompt de Diplomeo (prod) vers Diplomeo dev
"""

import requests
import json

RAGFLOW_HOST = "https://rag-staging.flowkura.com"
API_KEY = "ragflow-d4iWypSjduSHlkWb-wFOwda57ytZFsE7sxc6npOt9b8"

CHAT_PROD_ID = "1098c60ff69f11f0965902420a000115"  # Diplomeo
CHAT_DEV_ID = "26508f5afbf511f08df602420a000115"   # Diplomeo dev

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_chat_config(chat_id):
    """Récupérer la configuration d'un chat"""
    url = f"{RAGFLOW_HOST}/api/v1/chats"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        for chat in data.get('data', []):
            if chat['id'] == chat_id:
                return chat
    return None

def main():
    print("🔍 Récupération du prompt de Diplomeo (prod)...")
    
    prod_config = get_chat_config(CHAT_PROD_ID)
    if not prod_config:
        print("❌ Impossible de récupérer la config de Diplomeo prod")
        return
    
    prompt_prod = prod_config['prompt']['prompt']
    print(f"✅ Prompt récupéré ({len(prompt_prod)} caractères)")
    
    # Vérifier que c'est bien le nouveau prompt
    if "RÈGLE CRITIQUE" in prompt_prod:
        print("✅ Le prompt contient bien la RÈGLE CRITIQUE")
    else:
        print("⚠️  Attention: le prompt ne contient pas la RÈGLE CRITIQUE")
    
    print("\n📝 Sauvegarde du prompt dans un fichier...")
    with open('prompt_from_prod.txt', 'w', encoding='utf-8') as f:
        f.write(prompt_prod)
    print("✅ Sauvegardé dans: prompt_from_prod.txt")
    
    print("\n" + "="*80)
    print("INSTRUCTION MANUELLE")
    print("="*80)
    print("\nLe prompt de prod a été sauvegardé dans 'prompt_from_prod.txt'")
    print("\nPour mettre à jour Diplomeo dev:")
    print("1. cat prompt_from_prod.txt | wl-copy")
    print("2. Dans RAGFlow, ouvrir 'Diplomeo dev'")
    print("3. Coller le prompt")
    print("4. Sauvegarder")
    print("\nSi le bouton Save ne fonctionne pas, il y a peut-être un bug avec ce chat.")
    print("Vous pouvez aussi essayer de:")
    print("- Rafraîchir la page (F5)")
    print("- Supprimer et recréer 'Diplomeo dev'")
    print("- Contacter le support RAGFlow")

if __name__ == "__main__":
    main()
