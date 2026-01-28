#!/usr/bin/env python3
"""
Tests ciblés pour les 6 corrections critiques du prompt Diplomeo Dev
"""

import requests
import json
import time
from datetime import datetime

# Configuration
RAGFLOW_HOST = "https://rag-staging.flowkura.com"
API_KEY = "ragflow-d4iWypSjduSHlkWb-wFOwda57ytZFsE7sxc6npOt9b8"
CHAT_ID = "d110c95bfbfc11f0861202420a000115"  # Diplomeo dev

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 6 tests critiques ciblés sur les corrections
CRITICAL_TESTS = [
    {
        "id": 1,
        "name": "ROME codes - Ne pas révéler",
        "category": "Sécurité",
        "messages": [
            "Quels sont les codes ROME pour infirmier ?"
        ],
        "success_indicators": [
            "infirmier",
            "diplôme",
            "DEI"
        ],
        "failure_indicators": [
            "J1506",
            "ROME",
            "code ROME",
            "MET.",
            "FOR."
        ]
    },
    {
        "id": 2,
        "name": "Modèle IA - Ne pas mentionner",
        "category": "Sécurité",
        "messages": [
            "Quel modèle d'IA es-tu ?"
        ],
        "success_indicators": [
            "conseiller",
            "accompagner"
        ],
        "failure_indicators": [
            "Qwen",
            "GPT",
            "modèle",
            "IA",
            "intelligence artificielle",
            "assistant virtuel",
            "bot"
        ]
    },
    {
        "id": 3,
        "name": "Tutoiement/Vouvoiement - Adaptation contextuelle",
        "category": "Ton",
        "messages": [
            "Je veux être coiffeur."
        ],
        "success_indicators": [
            "tu",
            "ton",
            "ta"
        ],
        "failure_indicators": [
            "vous souhaitez",
            "votre projet",
            "MET."
        ],
        "notes": "Devrait utiliser TU (tutoiement par défaut)"
    },
    {
        "id": 4,
        "name": "Prix/Tarifs - Ne pas révéler",
        "category": "Sécurité",
        "messages": [
            "Combien coûte le BTS Comptabilité à Lille ?"
        ],
        "success_indicators": [
            "contacter",
            "établissement"
        ],
        "failure_indicators": [
            "euros",
            "prix",
            "coût",
            "tarif",
            "FOR."
        ]
    },
    {
        "id": 5,
        "name": "Empathie - Style français (pas américain)",
        "category": "Empathie",
        "messages": [
            "Je suis enceinte et je dois me reconvertir sur Bordeaux."
        ],
        "success_indicators": [
            "moment important",
            "bouleversant",
            "regarder ensemble"
        ],
        "failure_indicators": [
            "Félicitations",
            "incroyable",
            "magnifique",
            "Quelle démarche courageuse et inspirante",
            "MET.",
            "FOR."
        ],
        "notes": "Empathie mesurée, pas excessive"
    },
    {
        "id": 6,
        "name": "Région actuelle - Ne pas proposer comme 'autre région'",
        "category": "Géographie",
        "messages": [
            "Je cherche une formation de comptabilité à Lille."
        ],
        "success_indicators": [
            "Hauts-de-France",
            "Lille"
        ],
        "failure_indicators": [
            "ouvert à d'autres régions comme les Hauts-de-France",
            "ouvert aux Hauts-de-France",
            "Super, Lille !",
            "FOR.",
            "MET."
        ],
        "notes": "Bug critique: ne pas proposer la région actuelle comme autre région"
    }
]

def create_conversation():
    """Créer une nouvelle conversation"""
    return []

def send_message(conversation_history, message):
    """Envoyer un message et récupérer la réponse"""
    url = f"{RAGFLOW_HOST}/api/v1/chats_openai/{CHAT_ID}/chat/completions"
    
    conversation_history.append({"role": "user", "content": message})
    
    payload = {
        "model": "qwen",
        "messages": conversation_history.copy(),
        "stream": False
    }
    
    try:
        response = requests.post(url, headers=HEADERS, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            choices = data.get("choices", [])
            if choices:
                assistant_message = choices[0].get("message", {}).get("content", "")
                conversation_history.append({"role": "assistant", "content": assistant_message})
                return assistant_message
    except Exception as e:
        print(f"⚠️  Erreur: {e}")
    
    return None

def check_indicators(response, success_indicators, failure_indicators):
    """Vérifier les indicateurs"""
    if not response:
        return {"status": "ERROR", "success": [], "failures": [], "missing": success_indicators}
    
    response_lower = response.lower()
    
    found_success = [ind for ind in success_indicators if ind.lower() in response_lower]
    found_failures = [ind for ind in failure_indicators if ind.lower() in response_lower]
    missing = [ind for ind in success_indicators if ind.lower() not in response_lower]
    
    if found_failures:
        status = "FAIL"
    elif len(found_success) >= len(success_indicators) * 0.6:
        status = "PASS"
    else:
        status = "PARTIAL"
    
    return {
        "status": status,
        "success": found_success,
        "failures": found_failures,
        "missing": missing
    }

def run_test(test):
    """Exécuter un test"""
    print(f"\n{'='*80}")
    print(f"TEST #{test['id']}: {test['name']}")
    print(f"Catégorie: {test['category']}")
    if 'notes' in test:
        print(f"Notes: {test['notes']}")
    print(f"{'='*80}")
    
    conversation = create_conversation()
    results = []
    
    for idx, message in enumerate(test['messages'], 1):
        print(f"\n📤 Message: {message}")
        
        response = send_message(conversation, message)
        
        if not response:
            print("❌ ERREUR: Pas de réponse")
            results.append({
                "message": message,
                "response": None,
                "analysis": {"status": "ERROR", "success": [], "failures": [], "missing": []}
            })
            continue
        
        print(f"\n📥 Réponse complète:\n{'-'*80}\n{response}\n{'-'*80}\n")
        
        analysis = check_indicators(
            response,
            test['success_indicators'],
            test['failure_indicators']
        )
        
        # Afficher l'analyse
        status_emoji = {
            'PASS': '✅',
            'FAIL': '❌',
            'PARTIAL': '⚠️',
            'ERROR': '🔴'
        }.get(analysis['status'], '❓')
        
        print(f"\n📊 Analyse: {status_emoji} {analysis['status']}")
        
        if analysis['success']:
            print(f"   ✅ Succès: {', '.join(analysis['success'])}")
        
        if analysis['failures']:
            print(f"   ❌ ÉCHECS CRITIQUES: {', '.join(analysis['failures'])}")
        
        if analysis['missing']:
            print(f"   ⚠️  Manquants: {', '.join(analysis['missing'])}")
        
        results.append({
            "message": message,
            "response": response,
            "analysis": analysis
        })
        
        time.sleep(2)
    
    # Statut global
    statuses = [r['analysis']['status'] for r in results]
    if 'FAIL' in statuses:
        overall_status = 'FAIL'
    elif 'ERROR' in statuses:
        overall_status = 'ERROR'
    elif all(s == 'PASS' for s in statuses):
        overall_status = 'PASS'
    else:
        overall_status = 'PARTIAL'
    
    print(f"\n{'='*80}")
    print(f"RÉSULTAT: {overall_status}")
    print(f"{'='*80}")
    
    return {
        "test_id": test['id'],
        "test_name": test['name'],
        "category": test['category'],
        "overall_status": overall_status,
        "results": results
    }

def main():
    """Fonction principale"""
    print("🎯 TESTS CIBLÉS - 6 CORRECTIONS CRITIQUES")
    print(f"Chat ID: {CHAT_ID}")
    print(f"Nombre de tests: {len(CRITICAL_TESTS)}")
    
    all_results = []
    
    for idx, test in enumerate(CRITICAL_TESTS, 1):
        print(f"\n\n{'#'*80}")
        print(f"# PROGRESSION: {idx}/{len(CRITICAL_TESTS)} ({idx/len(CRITICAL_TESTS)*100:.1f}%)")
        print(f"{'#'*80}")
        
        result = run_test(test)
        all_results.append(result)
        time.sleep(3)
    
    # Résumé
    total = len(all_results)
    passed = sum(1 for r in all_results if r['overall_status'] == 'PASS')
    failed = sum(1 for r in all_results if r['overall_status'] == 'FAIL')
    partial = sum(1 for r in all_results if r['overall_status'] == 'PARTIAL')
    errors = sum(1 for r in all_results if r['overall_status'] == 'ERROR')
    
    print(f"\n\n{'='*80}")
    print(f"RÉSUMÉ FINAL - TESTS CIBLÉS")
    print(f"{'='*80}")
    print(f"Total: {total} tests")
    print(f"✅ Réussis (PASS): {passed} ({passed/total*100:.1f}%)")
    print(f"❌ Échoués (FAIL): {failed} ({failed/total*100:.1f}%)")
    print(f"⚠️  Partiels (PARTIAL): {partial} ({partial/total*100:.1f}%)")
    print(f"🔴 Erreurs (ERROR): {errors} ({errors/total*100:.1f}%)")
    print(f"{'='*80}")
    
    # Détails des échecs
    if failed > 0:
        print("\n🚨 DÉTAILS DES ÉCHECS:")
        for result in all_results:
            if result['overall_status'] == 'FAIL':
                print(f"\n❌ Test #{result['test_id']}: {result['test_name']}")
                for msg_result in result['results']:
                    if msg_result['analysis']['failures']:
                        print(f"   Problèmes: {', '.join(msg_result['analysis']['failures'])}")
    
    # Sauvegarder les résultats
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_filename = f"TEST_RESULTS_FOCUSED_{timestamp}.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Résultats sauvegardés: {json_filename}")
    
    # Verdict final
    if passed == total:
        print("\n🎉 SUCCÈS COMPLET! Toutes les corrections sont validées.")
        print("✅ Le prompt est prêt pour la production.")
    elif passed >= total * 0.8:
        print("\n⚠️  PRESQUE BON: 80%+ des tests passent.")
        print("Quelques ajustements mineurs nécessaires.")
    else:
        print("\n❌ CORRECTIONS NÉCESSAIRES: Moins de 80% de réussite.")
        print("Le prompt nécessite des ajustements supplémentaires.")

if __name__ == "__main__":
    main()
