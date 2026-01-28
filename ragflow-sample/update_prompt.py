#!/usr/bin/env python3
"""
Script pour mettre à jour le prompt du chat dev
"""

import requests
import json

RAGFLOW_HOST = "https://rag-staging.flowkura.com"
API_KEY = "ragflow-d4iWypSjduSHlkWb-wFOwda57ytZFsE7sxc6npOt9b8"
CHAT_ID = "26508f5afbf511f08df602420a000115"  # Diplomeo dev

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def update_prompt():
    """Mettre à jour le prompt du chat"""
    # Lire le prompt
    with open('system_prompt_dev_v2.txt', 'r', encoding='utf-8') as f:
        prompt = f.read()
    
    url = f"{RAGFLOW_HOST}/api/v1/chats/{CHAT_ID}"
    
    payload = {
        "prompt": prompt
    }
    
    print(f"Mise à jour du chat {CHAT_ID}...")
    print(f"Longueur du prompt: {len(prompt)} caractères")
    
    response = requests.put(url, headers=HEADERS, json=payload)
    
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('code') == 0:
            print("✅ Prompt mis à jour avec succès!")
            return True
        else:
            print(f"❌ Erreur: {data.get('message')}")
            return False
    else:
        print(f"❌ Erreur HTTP: {response.status_code}")
        return False

if __name__ == "__main__":
    update_prompt()
