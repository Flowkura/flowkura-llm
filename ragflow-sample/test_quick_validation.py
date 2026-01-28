#!/usr/bin/env python3
"""
Test rapide de 5 scénarios critiques pour valider les corrections
"""

import requests
import json
import time

RAGFLOW_HOST = "https://rag-staging.flowkura.com"
API_KEY = "ragflow-d4iWypSjduSHlkWb-wFOwda57ytZFsE7sxc6npOt9b8"
CHAT_ID = "26508f5afbf511f08df602420a000115"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

QUICK_TESTS = [
    {
        "name": "Bug région Lille",
        "query": "Je cherche une formation de comptabilité à Lille.",
        "check": lambda r: not ("ouvert à d'autres régions comme les hauts-de-france" in r.lower() or "ouvert aux hauts-de-france" in r.lower()),
        "description": "Ne doit PAS proposer les Hauts-de-France comme 'autre région' pour Lille"
    },
    {
        "name": "Bug région Bordeaux",
        "query": "Je veux faire une formation à Bordeaux.",
        "check": lambda r: not ("ouvert à d'autres régions comme la nouvelle-aquitaine" in r.lower() or "ouvert à la nouvelle-aquitaine" in r.lower()),
        "description": "Ne doit PAS proposer la Nouvelle-Aquitaine comme 'autre région' pour Bordeaux"
    },
    {
        "name": "Empathie grossesse",
        "query": "Je suis enceinte et je dois me reconvertir.",
        "check": lambda r: "félicitations" not in r.lower() and ("moment important" in r.lower() or "bouleversant" in r.lower() or "sécuriser" in r.lower()),
        "description": "Doit montrer empathie sans dire 'Félicitations'"
    },
    {
        "name": "Pas de codes techniques",
        "query": "Je veux être infirmier à Lille.",
        "check": lambda r: "met." not in r.lower() and "for." not in r.lower() and "uai" not in r.lower(),
        "description": "Ne doit PAS révéler les codes techniques"
    },
    {
        "name": "Vouvoiement",
        "query": "Je veux être coiffeur.",
        "check": lambda r: ("vous" in r.lower() or "votre" in r.lower()) and "tu " not in r.lower() and "ton " not in r.lower(),
        "description": "Doit utiliser le vouvoiement"
    }
]

def send_message(query):
    """Envoyer un message et récupérer la réponse"""
    url = f"{RAGFLOW_HOST}/api/v1/chats_openai/{CHAT_ID}/chat/completions"
    
    payload = {
        "model": "qwen",
        "messages": [{"role": "user", "content": query}],
        "stream": False
    }
    
    try:
        response = requests.post(url, headers=HEADERS, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            choices = data.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "")
    except Exception as e:
        print(f"Erreur: {e}")
    
    return None

def run_quick_tests():
    """Exécuter les tests rapides"""
    print("🚀 TESTS RAPIDES DE VALIDATION\n")
    print("=" * 80)
    
    results = []
    
    for idx, test in enumerate(QUICK_TESTS, 1):
        print(f"\n[{idx}/{len(QUICK_TESTS)}] {test['name']}")
        print("-" * 80)
        print(f"Query: {test['query']}")
        print(f"Check: {test['description']}")
        print("\nEnvoi...")
        
        response = send_message(test['query'])
        
        if not response:
            print("❌ ERREUR: Pas de réponse")
            results.append({"test": test['name'], "status": "ERROR", "response": None})
            continue
        
        # Afficher la réponse (tronquée)
        print(f"\nRéponse (300 premiers caractères):")
        print(response[:300] + ("..." if len(response) > 300 else ""))
        
        # Vérifier
        passed = test['check'](response)
        
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"\nRésultat: {status}")
        
        results.append({
            "test": test['name'],
            "status": "PASS" if passed else "FAIL",
            "response": response
        })
        
        print("=" * 80)
        
        # Pause
        time.sleep(2)
    
    # Résumé
    print("\n\n" + "=" * 80)
    print("RÉSUMÉ")
    print("=" * 80)
    
    total = len(results)
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    errors = sum(1 for r in results if r['status'] == 'ERROR')
    
    print(f"Total: {total}")
    print(f"✅ Réussis: {passed} ({passed/total*100:.0f}%)")
    print(f"❌ Échoués: {failed} ({failed/total*100:.0f}%)")
    print(f"🔴 Erreurs: {errors}")
    
    if failed > 0:
        print("\n⚠️  Tests échoués:")
        for r in results:
            if r['status'] == 'FAIL':
                print(f"  - {r['test']}")
    
    print("=" * 80)
    
    return results

if __name__ == "__main__":
    run_quick_tests()
