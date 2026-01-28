#!/usr/bin/env python3
"""
Suite de tests exhaustive pour le chat Flowkura Diplomeo
Couvre tous les cas limites et scénarios réels
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

# Suite exhaustive de scénarios
SCENARIOS = [
    # ==========================================
    # CATÉGORIE 1 : ENTONNOIR GÉOGRAPHIQUE
    # ==========================================
    {
        "id": 1,
        "category": "Géographie",
        "name": "Ville → Région : Lille (Hauts-de-France)",
        "messages": [
            "Je cherche une formation de comptabilité à Lille."
        ],
        "success_indicators": [
            "Hauts-de-France",
            "Lille"
        ],
        "failure_indicators": [
            "Super, Lille !",
            "êtes-vous ouvert à d'autres régions comme les Hauts-de-France",
            "ouvert aux Hauts-de-France",
            "FOR.",
            "AF."
        ]
    },
    {
        "id": 2,
        "category": "Géographie",
        "name": "Ville → Région : Bordeaux (Nouvelle-Aquitaine)",
        "messages": [
            "Je veux faire une formation à Bordeaux."
        ],
        "success_indicators": [
            "Nouvelle-Aquitaine",
            "Bordeaux"
        ],
        "failure_indicators": [
            "ouvert à d'autres régions comme la Nouvelle-Aquitaine",
            "Super, Bordeaux !",
            "FOR.",
            "MET."
        ]
    },
    {
        "id": 3,
        "category": "Géographie",
        "name": "Ville → Région : Lyon (Auvergne-Rhône-Alpes)",
        "messages": [
            "Formation sur Lyon svp."
        ],
        "success_indicators": [
            "Auvergne-Rhône-Alpes",
            "Lyon"
        ],
        "failure_indicators": [
            "ouvert à d'autres régions comme Auvergne",
            "Super !",
            "FOR."
        ]
    },
    {
        "id": 4,
        "category": "Géographie",
        "name": "Ville inconnue / petite commune",
        "messages": [
            "Je cherche une formation à Trifouillis-les-Oies."
        ],
        "success_indicators": [
            "région",
            "préciser",
            "situe"
        ],
        "failure_indicators": [
            "FOR.",
            "code UAI"
        ]
    },
    {
        "id": 5,
        "category": "Géographie",
        "name": "Région directement (sans ville)",
        "messages": [
            "Je veux étudier en Bretagne."
        ],
        "success_indicators": [
            "Bretagne",
            "ville",
            "préciser"
        ],
        "failure_indicators": [
            "Super !",
            "FOR."
        ]
    },
    {
        "id": 6,
        "category": "Géographie",
        "name": "Multi-villes (mobilité géographique)",
        "messages": [
            "Je peux étudier à Lille ou à Paris."
        ],
        "success_indicators": [
            "Hauts-de-France",
            "Île-de-France"
        ],
        "failure_indicators": [
            "FOR.",
            "MET."
        ]
    },
    
    # ==========================================
    # CATÉGORIE 2 : EMPATHIE & SITUATIONS DE VIE
    # ==========================================
    {
        "id": 7,
        "category": "Empathie",
        "name": "Grossesse / Maternité",
        "messages": [
            "Je suis enceinte et je dois me reconvertir sur Bordeaux."
        ],
        "success_indicators": [
            "moment important",
            "bouleversant",
            "sécuriser",
            "Nouvelle-Aquitaine"
        ],
        "failure_indicators": [
            "Félicitations",
            "Super !",
            "Génial",
            "FOR.",
            "MET."
        ]
    },
    {
        "id": 8,
        "category": "Empathie",
        "name": "Chômage / Reconversion",
        "messages": [
            "Je suis au chômage depuis 6 mois, je veux me former à Nancy."
        ],
        "success_indicators": [
            "courageuse",
            "démarche",
            "Grand Est",
            "Nancy"
        ],
        "failure_indicators": [
            "dommage",
            "désolé",
            "FOR."
        ]
    },
    {
        "id": 9,
        "category": "Empathie",
        "name": "Fatigue / Burn-out",
        "messages": [
            "Je suis épuisé par mon travail actuel, je cherche une reconversion."
        ],
        "success_indicators": [
            "comprends",
            "période",
            "réflexions"
        ],
        "failure_indicators": [
            "courage",
            "faut tenir",
            "FOR."
        ]
    },
    {
        "id": 10,
        "category": "Empathie",
        "name": "Empathie PUIS géographie (ordre important)",
        "messages": [
            "Je suis enceinte et je cherche une formation d'aide-soignante à Rennes."
        ],
        "success_indicators": [
            "moment important",
            "Bretagne",
            "Rennes",
            "aide-soignante"
        ],
        "failure_indicators": [
            "Félicitations",
            "Super !",
            "FOR."
        ]
    },
    
    # ==========================================
    # CATÉGORIE 3 : CHAÎNE DE LEAD COMPLÈTE
    # ==========================================
    {
        "id": 11,
        "category": "Lead Chain",
        "name": "Métier → Formation → Région → Établissement (Infirmier)",
        "messages": [
            "Je veux être infirmier à Lille."
        ],
        "success_indicators": [
            "infirmier",
            "Hauts-de-France",
            "Lille",
            "3 ans",
            "établissements"
        ],
        "failure_indicators": [
            "MET.700",
            "FOR.2378",
            "code UAI",
            "Voici les écoles",
            "ouvert à d'autres régions comme les Hauts-de-France"
        ]
    },
    {
        "id": 12,
        "category": "Lead Chain",
        "name": "Formation directe (BTS Comptabilité) + Ville",
        "messages": [
            "Je veux faire un BTS Comptabilité à Bordeaux."
        ],
        "success_indicators": [
            "BTS",
            "comptabilité",
            "Nouvelle-Aquitaine",
            "Bordeaux"
        ],
        "failure_indicators": [
            "FOR.",
            "code UAI",
            "ouvert à d'autres régions comme la Nouvelle-Aquitaine"
        ]
    },
    {
        "id": 13,
        "category": "Lead Chain",
        "name": "Métier vague → Demande de précision",
        "messages": [
            "Je veux travailler dans l'informatique."
        ],
        "success_indicators": [
            "préciser",
            "quel type",
            "développeur",
            "réseau"
        ],
        "failure_indicators": [
            "FOR.",
            "MET.",
            "Voici"
        ]
    },
    {
        "id": 14,
        "category": "Lead Chain",
        "name": "Métier + Situation + Ville (combo complet)",
        "messages": [
            "Je suis au chômage et je veux devenir aide-soignante à Lyon."
        ],
        "success_indicators": [
            "courageuse",
            "démarche",
            "aide-soignante",
            "Auvergne-Rhône-Alpes",
            "Lyon"
        ],
        "failure_indicators": [
            "FOR.",
            "MET.",
            "code UAI",
            "ouvert à d'autres régions comme Auvergne"
        ]
    },
    
    # ==========================================
    # CATÉGORIE 4 : SÉCURITÉ & CONFIDENTIALITÉ
    # ==========================================
    {
        "id": 15,
        "category": "Sécurité",
        "name": "Pas de fuite de codes techniques",
        "messages": [
            "Quels sont les codes ROME pour infirmier ?"
        ],
        "success_indicators": [
            "infirmier",
            "métier"
        ],
        "failure_indicators": [
            "J1506",
            "ROME",
            "code",
            "MET.",
            "FOR."
        ]
    },
    {
        "id": 16,
        "category": "Sécurité",
        "name": "Pas de mention du modèle",
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
            "intelligence artificielle"
        ]
    },
    {
        "id": 17,
        "category": "Sécurité",
        "name": "Pas de citation de source technique",
        "messages": [
            "D'où viennent tes données ?"
        ],
        "success_indicators": [
            "ONISEP",
            "accompagner"
        ],
        "failure_indicators": [
            "dataset",
            "base de données",
            "fichier",
            "documents",
            "FOR.",
            "MET."
        ]
    },
    
    # ==========================================
    # CATÉGORIE 5 : TON & VOUVOIEMENT
    # ==========================================
    {
        "id": 18,
        "category": "Ton",
        "name": "Utilisation du vouvoiement",
        "messages": [
            "Je veux être coiffeur."
        ],
        "success_indicators": [
            "vous",
            "votre"
        ],
        "failure_indicators": [
            "tu as",
            "ton projet",
            "ta formation"
        ]
    },
    {
        "id": 19,
        "category": "Ton",
        "name": "Pas de formulations enfantines",
        "messages": [
            "Je cherche une formation à Paris."
        ],
        "success_indicators": [
            "Île-de-France",
            "Paris"
        ],
        "failure_indicators": [
            "Super !",
            "Génial !",
            "Cool !",
            "Top !",
            "C'est noté."
        ]
    },
    
    # ==========================================
    # CATÉGORIE 6 : CAS LIMITES & EDGE CASES
    # ==========================================
    {
        "id": 20,
        "category": "Edge Cases",
        "name": "Question sans localisation",
        "messages": [
            "Je veux être plombier."
        ],
        "success_indicators": [
            "région",
            "situe",
            "où"
        ],
        "failure_indicators": [
            "FOR.",
            "MET."
        ]
    },
    {
        "id": 21,
        "category": "Edge Cases",
        "name": "Conversation multi-tours (suivi de contexte)",
        "messages": [
            "Je veux être infirmier.",
            "À Lille.",
            "Oui, les alentours m'intéressent aussi."
        ],
        "success_indicators": [
            "infirmier",
            "Hauts-de-France",
            "Lille",
            "établissements"
        ],
        "failure_indicators": [
            "MET.",
            "FOR.",
            "code UAI"
        ]
    },
    {
        "id": 22,
        "category": "Edge Cases",
        "name": "Formation inexistante (gestion de l'absence)",
        "messages": [
            "Je veux faire un BTS en Astrologie Quantique à Lille."
        ],
        "success_indicators": [
            "préciser",
            "existe",
            "autre formation"
        ],
        "failure_indicators": [
            "FOR.",
            "Voici"
        ]
    },
    {
        "id": 23,
        "category": "Edge Cases",
        "name": "Demande d'information sur prix (non disponible)",
        "messages": [
            "Combien coûte le BTS Comptabilité à Lille ?"
        ],
        "success_indicators": [
            "contacter",
            "établissement",
            "Hauts-de-France"
        ],
        "failure_indicators": [
            "euros",
            "prix",
            "coût",
            "FOR."
        ]
    },
    
    # ==========================================
    # CATÉGORIE 7 : FORMULATIONS PROFESSIONNELLES
    # ==========================================
    {
        "id": 24,
        "category": "Formulations",
        "name": "Transition établissements (pas 'Voici les écoles')",
        "messages": [
            "Montre-moi les écoles d'infirmiers à Lille."
        ],
        "success_indicators": [
            "sélectionné ces établissements",
            "établissements dans votre région",
            "Hauts-de-France"
        ],
        "failure_indicators": [
            "Voici les écoles",
            "Liste des écoles",
            "MET.",
            "FOR.",
            "code UAI",
            "ouvert à d'autres régions comme les Hauts-de-France"
        ]
    },
    {
        "id": 25,
        "category": "Formulations",
        "name": "Reformulation âge (pas 'C'est noté')",
        "messages": [
            "J'ai 25 ans et je cherche une formation à Bordeaux."
        ],
        "success_indicators": [
            "bon moment",
            "structurer",
            "projet",
            "Nouvelle-Aquitaine"
        ],
        "failure_indicators": [
            "C'est noté",
            "Ok",
            "D'accord, 25 ans",
            "FOR."
        ]
    }
]

def create_conversation():
    """Créer une nouvelle conversation - retourne une liste vide pour les messages"""
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
    
    try:
        response = requests.post(url, headers=HEADERS, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            choices = data.get("choices", [])
            if choices:
                assistant_message = choices[0].get("message", {}).get("content", "")
                # Ajouter la réponse de l'assistant à l'historique
                conversation_history.append({"role": "assistant", "content": assistant_message})
                return assistant_message
    except Exception as e:
        print(f"⚠️  Erreur lors de l'envoi: {e}")
    
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
    print(f"Catégorie: {scenario['category']}")
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
                "analysis": {"status": "ERROR", "success": [], "failures": [], "missing": []}
            })
            continue
        
        print(f"\n📥 Réponse:\n{response[:300]}{'...' if len(response) > 300 else ''}\n")
        
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
        time.sleep(2)
    
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
        "category": scenario['category'],
        "overall_status": overall_status,
        "results": results,
        "conversation_length": len(conversation)
    }

def generate_report(all_results):
    """Générer un rapport de test exhaustif"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# RAPPORT DE TEST EXHAUSTIF - FLOWKURA DIPLOMEO DEV
**Date**: {timestamp}  
**Chat ID**: {CHAT_ID}  
**Version du prompt**: v2 (corrigé bug région actuelle)

## 📊 Résumé Exécutif

"""
    
    # Compter les résultats
    total = len(all_results)
    passed = sum(1 for r in all_results if r['overall_status'] == 'PASS')
    failed = sum(1 for r in all_results if r['overall_status'] == 'FAIL')
    partial = sum(1 for r in all_results if r['overall_status'] == 'PARTIAL')
    errors = sum(1 for r in all_results if r['overall_status'] == 'ERROR')
    
    success_rate = (passed / total * 100) if total > 0 else 0
    
    report += f"""- **Total scénarios**: {total}
- **✅ Réussis (PASS)**: {passed} ({passed/total*100:.1f}%)
- **❌ Échoués (FAIL)**: {failed} ({failed/total*100:.1f}%)
- **⚠️  Partiels (PARTIAL)**: {partial} ({partial/total*100:.1f}%)
- **🔴 Erreurs (ERROR)**: {errors} ({errors/total*100:.1f}%)
- **📈 Taux de réussite**: {success_rate:.1f}%

"""
    
    # Résumé par catégorie
    categories = {}
    for result in all_results:
        cat = result.get('category', 'Unknown')
        if cat not in categories:
            categories[cat] = {'total': 0, 'passed': 0, 'failed': 0, 'partial': 0, 'error': 0}
        
        categories[cat]['total'] += 1
        status = result['overall_status']
        if status == 'PASS':
            categories[cat]['passed'] += 1
        elif status == 'FAIL':
            categories[cat]['failed'] += 1
        elif status == 'PARTIAL':
            categories[cat]['partial'] += 1
        else:
            categories[cat]['error'] += 1
    
    report += "## 📂 Résultats par Catégorie\n\n"
    report += "| Catégorie | Total | ✅ Pass | ❌ Fail | ⚠️ Partial | 🔴 Error | Taux |\n"
    report += "|:----------|------:|--------:|--------:|-----------:|---------:|-----:|\n"
    
    for cat, stats in sorted(categories.items()):
        rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
        report += f"| {cat} | {stats['total']} | {stats['passed']} | {stats['failed']} | {stats['partial']} | {stats['error']} | {rate:.0f}% |\n"
    
    report += "\n## 🔍 Détails par Scénario\n\n"
    
    # Regrouper par catégorie
    for cat in sorted(categories.keys()):
        report += f"### {cat}\n\n"
        
        cat_results = [r for r in all_results if r.get('category') == cat]
        
        for result in cat_results:
            status_emoji = {
                'PASS': '✅',
                'FAIL': '❌',
                'PARTIAL': '⚠️',
                'ERROR': '🔴'
            }.get(result['overall_status'], '❓')
            
            report += f"#### {status_emoji} Scénario #{result['scenario_id']}: {result['scenario_name']}\n\n"
            report += f"**Statut**: {result['overall_status']}  \n"
            report += f"**Messages échangés**: {result.get('conversation_length', 0)}\n\n"
            
            for idx, msg_result in enumerate(result.get('results', []), 1):
                report += f"**Message #{idx}**: {msg_result['message']}\n\n"
                
                # Afficher la réponse (tronquée si trop longue)
                response_text = msg_result['response'] or 'Pas de réponse'
                if len(response_text) > 500:
                    response_text = response_text[:500] + "...\n\n[Réponse tronquée]"
                
                report += f"**Réponse**:\n```\n{response_text}\n```\n\n"
                
                report += "**Analyse**:\n"
                report += f"- Statut: **{msg_result['analysis']['status']}**\n"
                
                if msg_result['analysis'].get('success'):
                    report += f"- ✅ Succès trouvés: {', '.join(msg_result['analysis']['success'])}\n"
                
                if msg_result['analysis'].get('failures'):
                    report += f"- ❌ **ÉCHECS CRITIQUES**: {', '.join(msg_result['analysis']['failures'])}\n"
                
                if msg_result['analysis'].get('missing'):
                    report += f"- ⚠️  Manquants: {', '.join(msg_result['analysis']['missing'])}\n"
                
                report += "\n"
            
            report += "---\n\n"
    
    # Synthèse des problèmes critiques
    critical_issues = []
    for result in all_results:
        if result['overall_status'] == 'FAIL':
            for msg_result in result['results']:
                if msg_result['analysis'].get('failures'):
                    critical_issues.append({
                        'scenario_id': result['scenario_id'],
                        'scenario_name': result['scenario_name'],
                        'failures': msg_result['analysis']['failures']
                    })
    
    if critical_issues:
        report += "## 🚨 Problèmes Critiques Détectés\n\n"
        for issue in critical_issues:
            report += f"- **Scénario #{issue['scenario_id']}** ({issue['scenario_name']}): {', '.join(issue['failures'])}\n"
        report += "\n"
    
    # Recommandations
    report += "## 💡 Recommandations\n\n"
    
    if success_rate >= 90:
        report += "✅ **Excellent** : Le système passe 90%+ des tests. Prêt pour la production.\n\n"
    elif success_rate >= 75:
        report += "⚠️  **Bon** : Le système passe 75%+ des tests. Quelques ajustements nécessaires avant production.\n\n"
    elif success_rate >= 50:
        report += "❌ **Moyen** : Le système passe seulement 50-75% des tests. Corrections importantes nécessaires.\n\n"
    else:
        report += "🔴 **Critique** : Le système échoue à plus de 50% des tests. Refonte majeure requise.\n\n"
    
    if critical_issues:
        report += "### Actions Prioritaires\n\n"
        
        # Analyser les types d'échecs
        failure_types = {}
        for issue in critical_issues:
            for failure in issue['failures']:
                if failure not in failure_types:
                    failure_types[failure] = 0
                failure_types[failure] += 1
        
        report += "**Échecs les plus fréquents**:\n"
        for failure, count in sorted(failure_types.items(), key=lambda x: x[1], reverse=True)[:5]:
            report += f"- `{failure}` ({count} occurrences)\n"
        
        report += "\n"
    
    report += "---\n\n"
    report += f"*Rapport généré automatiquement le {timestamp}*\n"
    
    return report

def main():
    """Fonction principale"""
    print("🚀 DÉMARRAGE DE LA SUITE DE TESTS EXHAUSTIVE")
    print(f"Chat ID: {CHAT_ID}")
    print(f"Nombre de scénarios: {len(SCENARIOS)}")
    print(f"Catégories: {len(set(s['category'] for s in SCENARIOS))}")
    
    # Demander confirmation
    print("\n⚠️  AVERTISSEMENT: Cette suite va exécuter 25 scénarios de test.")
    print("Cela peut prendre 10-15 minutes.")
    
    
    all_results = []
    
    for idx, scenario in enumerate(SCENARIOS, 1):
        print(f"\n\n{'#'*80}")
        print(f"# PROGRESSION: {idx}/{len(SCENARIOS)} ({idx/len(SCENARIOS)*100:.1f}%)")
        print(f"{'#'*80}")
        
        result = run_scenario(scenario)
        all_results.append(result)
        time.sleep(3)  # Pause entre les scénarios
    
    # Générer le rapport
    print("\n\n📝 Génération du rapport...")
    report = generate_report(all_results)
    
    # Sauvegarder le rapport
    report_filename = f"TEST_REPORT_EXHAUSTIVE_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Rapport sauvegardé: {report_filename}")
    
    # Sauvegarder les résultats bruts en JSON
    json_filename = f"TEST_RESULTS_EXHAUSTIVE_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Résultats JSON sauvegardés: {json_filename}")
    
    # Afficher le résumé
    total = len(all_results)
    passed = sum(1 for r in all_results if r['overall_status'] == 'PASS')
    failed = sum(1 for r in all_results if r['overall_status'] == 'FAIL')
    
    print(f"\n\n{'='*80}")
    print(f"RÉSUMÉ FINAL")
    print(f"{'='*80}")
    print(f"Total: {total} scénarios")
    print(f"✅ Réussis: {passed} ({passed/total*100:.1f}%)")
    print(f"❌ Échoués: {failed} ({failed/total*100:.1f}%)")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
