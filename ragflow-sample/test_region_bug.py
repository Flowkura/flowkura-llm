#!/usr/bin/env python3
"""
Test rapide du bug "région actuelle"
"""

import requests
import json

RAGFLOW_HOST = "https://rag-staging.flowkura.com"
API_KEY = "ragflow-d4iWypSjduSHlkWb-wFOwda57ytZFsE7sxc6npOt9b8"
CHAT_ID = "26508f5afbf511f08df602420a000115"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_region_bug():
    """Tester si le bug 'région actuelle' est corrigé"""
    url = f"{RAGFLOW_HOST}/api/v1/chats_openai/{CHAT_ID}/chat/completions"
    
    test_message = "Je cherche une formation de comptabilité à Lille."
    
    payload = {
        "model": "qwen",
        "messages": [{"role": "user", "content": test_message}],
        "stream": False
    }
    
    print(f"Test du message: {test_message}")
    print("Envoi...")
    
    response = requests.post(url, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        choices = data.get("choices", [])
        if choices:
            answer = choices[0].get("message", {}).get("content", "")
            
            print(f"\n{'='*80}")
            print("RÉPONSE:")
            print(f"{'='*80}")
            print(answer)
            print(f"{'='*80}\n")
            
            # Vérifier le bug
            answer_lower = answer.lower()
            
            print("ANALYSE DU BUG:")
            print("-" * 80)
            
            has_lille = "lille" in answer_lower
            has_region = "hauts-de-france" in answer_lower or "hauts de france" in answer_lower
            
            # Le bug: "ouvert à d'autres régions comme les Hauts-de-France"
            bug_phrase_1 = "ouvert" in answer_lower and "hauts" in answer_lower and "région" in answer_lower
            bug_phrase_2 = "autres régions comme" in answer_lower and "hauts" in answer_lower
            
            print(f"✓ Mentionne Lille: {has_lille}")
            print(f"✓ Mentionne Hauts-de-France: {has_region}")
            print(f"✗ Bug détecté (phrase 1): {bug_phrase_1}")
            print(f"✗ Bug détecté (phrase 2): {bug_phrase_2}")
            
            if bug_phrase_1 or bug_phrase_2:
                print("\n❌ BUG TOUJOURS PRÉSENT!")
                print("Le système propose les Hauts-de-France comme 'autre région' alors que Lille est DANS les Hauts-de-France.")
                return False
            else:
                print("\n✅ BUG CORRIGÉ!")
                print("Le système ne propose pas la région actuelle comme 'autre région'.")
                return True
    else:
        print(f"❌ Erreur HTTP: {response.status_code}")
        return False

if __name__ == "__main__":
    test_region_bug()
