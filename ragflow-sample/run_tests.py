#!/usr/bin/env python3
"""
Script de test automatisé pour le plan de test Flowkura
Test de l'entonnoir géographique et de la qualification des leads
"""

import requests
import json
import time
from datetime import datetime

# Configuration
RAGFLOW_HOST = "https://rag-staging.flowkura.com"
API_KEY = "ragflow-d4iWypSjduSHlkWb-wFOwda57ytZFsE7sxc6npOt9b8"
CHAT_ID = "26508f5afbf511f08df602420a000115"  # Diplomeo dev

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Scénarios de test
SCENARIOS = [
    {
        "id": 1,
        "name": "Test de l'entonnoir Régional (Lille)",
        "messages": [
            "Je cherche une formation de comptabilité à Lille."
        ],
        "success_indicators": [
            "Hauts-de-France",
            "Lille",
            "préférez rester strictement sur Lille ou les alentours"
        ],
        "failure_indicators": [
            "Super, Lille !",
            "FOR.",
            "AF.",
            "selon les documents"
        ]
    },
    {
        "id": 2,
        "name": "Test de l'Annonce de Vie (Empathie Française)",
        "messages": [
            "Je suis enceinte et je dois me reconvertir sur Bordeaux."
        ],
        "success_indicators": [
            "moment important",
            "Nouvelle-Aquitaine",
            "Bordeaux"
        ],
        "failure_indicators": [
            "Félicitations",
            "Super !",
            "FOR.",
            "code UAI"
        ]
    },
    {
        "id": 3,
        "name": "Test de Liaison : Métier → Formation → Région → Établissement",
        "messages": [
            "Je veux être infirmier à Lille."
        ],
        "success_indicators": [
            "infirmier",
            "Hauts-de-France",
            "Lille",
            "établissements",
            "3 ans"
        ],
        "failure_indicators": [
            "MET.700",
            "FOR.2378",
            "code UAI",
            "Voici les écoles"
        ]
    }
]

def create_conversation():
    """Créer une nouvelle conversation - retourne une liste vide pour les messages"""
    # Pour l'API OpenAI compatible, on gère l'historique manuellement
    return []

def send_message(conversation_history, message):
    """Envoyer un message et récupérer la réponse via l'API OpenAI compatible"""
    url = f"{RAGFLOW_HOST}/api/v1/chats_openai/{CHAT_ID}/chat/completions"
    
    # Ajouter le message de l'utilisateur à l'historique
    conversation_history.append({"role": "user", "content": message})
    
    payload = {
        "model": "qwen",
        "messages": conversation_history.copy(),
        "stream": False
    }
    
    response = requests.post(url, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        choices = data.get("choices", [])
        if choices:
            assistant_message = choices[0].get("message", {}).get("content", "")
            # Ajouter la réponse de l'assistant à l'historique
            conversation_history.append({"role": "assistant", "content": assistant_message})
            return assistant_message
    return None

def check_indicators(response, success_indicators, failure_indicators):
    """Vérifier les indicateurs de succès et d'échec"""
    if not response:
        return {"status": "ERROR", "success": [], "failures": [], "missing": success_indicators}
    
    response_lower = response.lower()
    
    # Indicateurs de succès trouvés
    found_success = [ind for ind in success_indicators if ind.lower() in response_lower]
    
    # Indicateurs d'échec trouvés (BAD!)
    found_failures = [ind for ind in failure_indicators if ind.lower() in response_lower]
    
    # Indicateurs manquants
    missing = [ind for ind in success_indicators if ind.lower() not in response_lower]
    
    # Déterminer le statut
    if found_failures:
        status = "FAIL"
    elif len(found_success) >= len(success_indicators) * 0.6:  # Au moins 60% des indicateurs
        status = "PASS"
    else:
        status = "PARTIAL"
    
    return {
        "status": status,
        "success": found_success,
        "failures": found_failures,
        "missing": missing
    }

def run_scenario(scenario):
    """Exécuter un scénario de test"""
    print(f"\n{'='*80}")
    print(f"SCÉNARIO #{scenario['id']}: {scenario['name']}")
    print(f"{'='*80}")
    
    # Créer une nouvelle conversation (historique de messages)
    conversation = create_conversation()
    
    print(f"✅ Nouvelle conversation initialisée")
    
    results = []
    
    for idx, message in enumerate(scenario['messages'], 1):
        print(f"\n📤 Message #{idx}: {message}")
        
        # Envoyer le message
        response = send_message(conversation, message)
        
        if not response:
            print("❌ ERREUR: Pas de réponse du serveur")
            results.append({
                "message": message,
                "response": None,
                "analysis": {"status": "ERROR"}
            })
            continue
        
        print(f"\n📥 Réponse:\n{response}\n")
        
        # Analyser la réponse
        analysis = check_indicators(
            response,
            scenario['success_indicators'],
            scenario['failure_indicators']
        )
        
        # Afficher l'analyse
        print(f"\n📊 Analyse:")
        print(f"   Statut: {analysis['status']}")
        
        if analysis['success']:
            print(f"   ✅ Indicateurs de succès trouvés: {', '.join(analysis['success'])}")
        
        if analysis['failures']:
            print(f"   ❌ Indicateurs d'échec trouvés: {', '.join(analysis['failures'])}")
        
        if analysis['missing']:
            print(f"   ⚠️  Indicateurs manquants: {', '.join(analysis['missing'])}")
        
        results.append({
            "message": message,
            "response": response,
            "analysis": analysis
        })
        
        # Pause entre les messages
        time.sleep(1)
    
    # Statut global du scénario
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
        "scenario_id": scenario['id'],
        "scenario_name": scenario['name'],
        "overall_status": overall_status,
        "results": results,
        "conversation_length": len(conversation)
    }

def generate_report(all_results):
    """Générer un rapport de test"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""
# RAPPORT DE TEST - FLOWKURA DIPLOMEO DEV
**Date**: {timestamp}
**Chat ID**: {CHAT_ID}

## Résumé Exécutif

"""
    
    # Compter les résultats
    total = len(all_results)
    passed = sum(1 for r in all_results if r['overall_status'] == 'PASS')
    failed = sum(1 for r in all_results if r['overall_status'] == 'FAIL')
    partial = sum(1 for r in all_results if r['overall_status'] == 'PARTIAL')
    errors = sum(1 for r in all_results if r['overall_status'] == 'ERROR')
    
    report += f"""
- **Total scénarios**: {total}
- **✅ Réussis**: {passed}
- **❌ Échoués**: {failed}
- **⚠️  Partiels**: {partial}
- **🔴 Erreurs**: {errors}

## Détails par Scénario

"""
    
    for result in all_results:
        status_emoji = {
            'PASS': '✅',
            'FAIL': '❌',
            'PARTIAL': '⚠️',
            'ERROR': '🔴'
        }.get(result['overall_status'], '❓')
        
        report += f"""
### {status_emoji} Scénario #{result['scenario_id']}: {result['scenario_name']}

**Statut**: {result['overall_status']}  
**Messages échangés**: {result.get('conversation_length', 0)}

"""
        
        for idx, msg_result in enumerate(result.get('results', []), 1):
            report += f"""
#### Message #{idx}
**Question**: {msg_result['message']}

**Réponse**:
```
{msg_result['response'] or 'Pas de réponse'}
```

**Analyse**:
- Statut: {msg_result['analysis']['status']}
"""
            
            if msg_result['analysis'].get('success'):
                report += f"- ✅ Succès: {', '.join(msg_result['analysis']['success'])}\n"
            
            if msg_result['analysis'].get('failures'):
                report += f"- ❌ Échecs: {', '.join(msg_result['analysis']['failures'])}\n"
            
            if msg_result['analysis'].get('missing'):
                report += f"- ⚠️  Manquants: {', '.join(msg_result['analysis']['missing'])}\n"
            
            report += "\n---\n"
    
    report += """
## Grille de Validation Linguistique & Géo

| Situation | Phrase à proscrire | Phrase attendue | Statut |
|:----------|:-------------------|:----------------|:-------|
"""
    
    # Ajouter les vérifications de la grille
    for result in all_results:
        scenario_id = result['scenario_id']
        status = result['overall_status']
        status_icon = '✅' if status == 'PASS' else '❌' if status == 'FAIL' else '⚠️'
        
        if scenario_id == 1:
            report += f"| Saisie de Lille | \"Super, Lille !\" | \"D'accord, à Lille. Je vais regarder dans les Hauts-de-France...\" | {status_icon} |\n"
        elif scenario_id == 2:
            report += f"| Annonce de vie | \"Félicitations !\" | \"C'est un moment important...\" | {status_icon} |\n"
        elif scenario_id == 3:
            report += f"| Transition Géo | \"Voici les écoles.\" | \"J'ai sélectionné ces établissements...\" | {status_icon} |\n"
    
    return report

def main():
    """Fonction principale"""
    print("🚀 DÉMARRAGE DES TESTS FLOWKURA - DIPLOMEO DEV")
    print(f"Chat ID: {CHAT_ID}")
    print(f"Nombre de scénarios: {len(SCENARIOS)}")
    
    all_results = []
    
    for scenario in SCENARIOS:
        result = run_scenario(scenario)
        all_results.append(result)
        time.sleep(2)  # Pause entre les scénarios
    
    # Générer le rapport
    report = generate_report(all_results)
    
    # Sauvegarder le rapport
    report_filename = f"TEST_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n\n✅ Rapport sauvegardé: {report_filename}")
    
    # Sauvegarder les résultats bruts en JSON
    json_filename = f"TEST_RESULTS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Résultats JSON sauvegardés: {json_filename}")

if __name__ == "__main__":
    main()
