#!/usr/bin/env python3
"""
Script d'évaluation du RAG Flowkura avec Giskard RAGET
Génère un testset automatique et évalue la qualité des réponses du chat Diplomeo dev

Utilise UNIQUEMENT:
- Le dossier ragflow-sample/ comme base de connaissances
- Le chat Diplomeo dev (26508f5afbf511f08df602420a000115) sur Ragflow
"""

import os
import json
import requests
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# Configuration - Diplomeo dev chat
RAGFLOW_HOST = "https://rag-staging.flowkura.com"
RAGFLOW_API_KEY = "ragflow-d4iWypSjduSHlkWb-wFOwda57ytZFsE7sxc6npOt9b8"
CHAT_ID = "26508f5afbf511f08df602420a000115"  # Diplomeo dev

HEADERS = {
    "Authorization": f"Bearer {RAGFLOW_API_KEY}",
    "Content-Type": "application/json"
}


class RagflowAgent:
    """Wrapper pour l'agent Ragflow Diplomeo dev compatible avec Giskard"""
    
    def __init__(self, host: str, api_key: str, chat_id: str):
        self.host = host
        self.api_key = api_key
        self.chat_id = chat_id
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def query(self, question: str, conversation_history: Optional[List[Dict]] = None) -> Dict[str, str]:
        """
        Interroge le chat Diplomeo dev et retourne la réponse
        
        Returns:
            Dict avec 'answer' et 'retrieved_contexts'
        """
        url = f"{self.host}/api/v1/chats_openai/{self.chat_id}/chat/completions"
        
        # Construire l'historique de conversation
        messages = conversation_history.copy() if conversation_history else []
        messages.append({"role": "user", "content": question})
        
        payload = {
            "model": "qwen",
            "messages": messages,
            "stream": False
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            choices = data.get("choices", [])
            
            if choices:
                answer = choices[0].get("message", {}).get("content", "")
                
                # Le contexte exact dépend de votre API Ragflow
                # Pour l'instant on le marque comme non disponible
                contexts = ["[Contexte via RAG Diplomeo dev]"]
                
                return {
                    "answer": answer,
                    "retrieved_contexts": contexts
                }
            else:
                return {
                    "answer": "[Aucune réponse]",
                    "retrieved_contexts": []
                }
                
        except Exception as e:
            print(f"❌ Erreur lors de la requête: {e}")
            return {
                "answer": f"[Erreur: {str(e)}]",
                "retrieved_contexts": []
            }
    
    def get_answer(self, question: str) -> str:
        """Méthode simplifiée pour Giskard - retourne juste la réponse"""
        result = self.query(question)
        return result["answer"]


def load_knowledge_base_from_ragflow_sample() -> pd.DataFrame:
    """
    Charge la base de connaissances depuis ragflow-sample/
    
    Structure du dossier:
    - 1_metiers/ : 9 métiers
    - 2_formations/ : 12 formations
    - 3_actions_formation/ : 41 actions de formation
    - 4_etablissements/ : (pas présent dans le listing mais mentionné)
    """
    knowledge_data = []
    base_path = Path("ragflow-sample")
    
    if not base_path.exists():
        print(f"❌ Erreur: Le dossier {base_path} n'existe pas")
        return pd.DataFrame()
    
    # Dossiers à scanner
    folders = {
        "1_metiers": "Métiers - Orientation France",
        "2_formations": "Formations - Orientation France", 
        "3_actions_formation": "Actions de Formation - Orientation France",
        "4_etablissements": "Établissements - Orientation France"
    }
    
    total_files = 0
    
    for folder_name, folder_desc in folders.items():
        folder_path = base_path / folder_name
        
        if not folder_path.exists():
            print(f"⚠️  Dossier {folder_name} non trouvé, passage au suivant")
            continue
        
        print(f"📂 Chargement de {folder_name}/...")
        md_files = list(folder_path.glob("*.md"))
        
        for md_file in md_files:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    knowledge_data.append({
                        "id": md_file.stem,
                        "content": content,
                        "category": folder_desc,
                        "filename": md_file.name,
                        "path": str(md_file)
                    })
                    total_files += 1
            except Exception as e:
                print(f"  ⚠️  Erreur lecture {md_file.name}: {e}")
        
        print(f"   ✓ {len(md_files)} fichiers chargés")
    
    df = pd.DataFrame(knowledge_data)
    print(f"\n✅ Base de connaissances chargée: {len(df)} documents au total")
    print(f"   Catégories: {df['category'].value_counts().to_dict()}")
    
    return df


def generate_testset_with_raget(knowledge_base: pd.DataFrame, num_questions: int = 30) -> object:
    """
    Génère un testset avec RAGET de Giskard
    
    Args:
        knowledge_base: DataFrame avec les documents de ragflow-sample/
        num_questions: Nombre de questions à générer (par défaut 30)
    
    Returns:
        QATestset de Giskard
    """
    try:
        from giskard.rag import generate_testset, KnowledgeBase
        
        print("\n" + "="*80)
        print("🪄 Génération du testset avec RAGET")
        print("="*80)
        
        if knowledge_base.empty:
            print("❌ La base de connaissances est vide")
            return None
        
        # Créer la base de connaissances Giskard
        print(f"📚 Initialisation de la base de connaissances ({len(knowledge_base)} documents)...")
        kb = KnowledgeBase.from_pandas(
            knowledge_base,
            columns=["content"]  # Colonne contenant le texte
        )
        
        print(f"🎲 Génération de {num_questions} questions/réponses...")
        print("   (Cela peut prendre plusieurs minutes selon votre LLM...)")
        print("   💡 Assurez-vous d'avoir configuré OPENAI_API_KEY dans votre environnement")
        
        # Générer le testset
        testset = generate_testset(
            kb,
            num_questions=num_questions,
            language='fr',  # Français
            agent_description=(
                "Diplomeo dev - Un chatbot d'orientation scolaire et professionnelle pour Flowkura. "
                "Il aide les utilisateurs à trouver des formations (BTS, Bac Pro, Diplômes d'État), "
                "des métiers, et des établissements en France selon leurs besoins géographiques "
                "et leurs projets professionnels. Le bot utilise un entonnoir géographique "
                "(Région → Département → Ville) et fait preuve d'empathie lors des annonces de vie."
            )
        )
        
        print(f"✅ Testset généré avec succès!")
        print(f"   - {len(testset)} questions générées")
        
        # Afficher un échantillon
        df = testset.to_pandas()
        print(f"\n📊 Aperçu du testset:")
        print(f"   - Types de questions: {df['metadata'].apply(lambda x: x.get('question_type', 'unknown')).value_counts().to_dict()}")
        
        return testset
        
    except ImportError as e:
        print(f"❌ Erreur d'import Giskard: {e}")
        print("   Assurez-vous que giskard[llm] est installé: pip install 'giskard[llm]'")
        return None
    except Exception as e:
        print(f"❌ Erreur lors de la génération du testset: {e}")
        import traceback
        traceback.print_exc()
        return None


def evaluate_rag_with_testset(agent: RagflowAgent, testset: object) -> pd.DataFrame:
    """
    Évalue le chat Diplomeo dev avec le testset généré
    
    Args:
        agent: Instance de RagflowAgent (chat Diplomeo dev)
        testset: QATestset de Giskard
    
    Returns:
        DataFrame avec les résultats d'évaluation
    """
    print("\n" + "="*80)
    print("📊 Évaluation du chat Diplomeo dev avec le testset")
    print("="*80)
    
    # Convertir le testset en DataFrame
    testset_df = testset.to_pandas()
    
    results = []
    
    for idx, row in testset_df.iterrows():
        question = row['question']
        reference_answer = row['reference_answer']
        reference_context = row['reference_context']
        metadata = row.get('metadata', {})
        
        print(f"\n[{idx + 1}/{len(testset_df)}] Question: {question[:80]}...")
        print(f"   Type: {metadata.get('question_type', 'unknown')}")
        
        # Obtenir la réponse du chat Diplomeo dev
        rag_result = agent.query(question)
        rag_answer = rag_result['answer']
        
        results.append({
            'question': question,
            'reference_answer': reference_answer,
            'reference_context': reference_context,
            'rag_answer': rag_answer,
            'retrieved_contexts': rag_result['retrieved_contexts'],
            'question_type': metadata.get('question_type', 'unknown'),
            'topic': metadata.get('topic', 'unknown')
        })
        
        print(f"   ✓ Réponse obtenue ({len(rag_answer)} caractères)")
    
    results_df = pd.DataFrame(results)
    print(f"\n✅ Évaluation terminée: {len(results_df)} questions traitées")
    
    return results_df


def analyze_results(results_df: pd.DataFrame) -> Dict:
    """
    Analyse basique des résultats (sans métriques RAGET avancées)
    """
    print("\n" + "="*80)
    print("📈 Analyse des résultats")
    print("="*80)
    
    # Statistiques basiques
    stats = {
        "total_questions": len(results_df),
        "avg_answer_length": results_df['rag_answer'].str.len().mean(),
        "questions_by_type": results_df['question_type'].value_counts().to_dict(),
        "empty_answers": (results_df['rag_answer'].str.strip() == "").sum(),
        "error_answers": results_df['rag_answer'].str.contains("Erreur|erreur").sum()
    }
    
    print(f"\n📊 Statistiques:")
    print(f"   Total de questions: {stats['total_questions']}")
    print(f"   Longueur moyenne des réponses: {stats['avg_answer_length']:.0f} caractères")
    print(f"   Réponses vides: {stats['empty_answers']}")
    print(f"   Réponses avec erreur: {stats['error_answers']}")
    print(f"\n   Questions par type:")
    for qtype, count in stats['questions_by_type'].items():
        print(f"      - {qtype}: {count}")
    
    return stats


def save_results(testset: object, results_df: pd.DataFrame, stats: Dict, output_dir: str = "giskard_results"):
    """Sauvegarde tous les résultats"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Sauvegarder le testset
    if testset:
        testset_file = output_path / f"testset_{timestamp}.jsonl"
        testset.save(str(testset_file))
        print(f"\n💾 Testset sauvegardé: {testset_file}")
    
    # Sauvegarder les résultats détaillés
    results_file = output_path / f"evaluation_results_{timestamp}.csv"
    results_df.to_csv(results_file, index=False, encoding='utf-8')
    print(f"💾 Résultats d'évaluation: {results_file}")
    
    # Sauvegarder les statistiques
    if stats:
        stats_file = output_path / f"stats_{timestamp}.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        print(f"💾 Statistiques: {stats_file}")
    
    # Créer un rapport Markdown
    report_file = output_path / f"report_{timestamp}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"# Rapport d'évaluation Giskard RAGET - Diplomeo dev\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Chat ID**: {CHAT_ID}\n\n")
        f.write(f"## Statistiques globales\n\n")
        f.write(f"- Total de questions: {stats['total_questions']}\n")
        f.write(f"- Longueur moyenne des réponses: {stats['avg_answer_length']:.0f} caractères\n")
        f.write(f"- Réponses vides: {stats['empty_answers']}\n")
        f.write(f"- Réponses avec erreur: {stats['error_answers']}\n\n")
        f.write(f"## Questions par type\n\n")
        for qtype, count in stats['questions_by_type'].items():
            f.write(f"- {qtype}: {count}\n")
        f.write(f"\n## Échantillon de questions/réponses\n\n")
        
        for idx, row in results_df.head(5).iterrows():
            f.write(f"### Question {idx + 1}\n\n")
            f.write(f"**Type**: {row['question_type']}\n\n")
            f.write(f"**Question**: {row['question']}\n\n")
            f.write(f"**Réponse du RAG**:\n{row['rag_answer']}\n\n")
            f.write(f"**Réponse de référence**:\n{row['reference_answer']}\n\n")
            f.write("---\n\n")
    
    print(f"💾 Rapport Markdown: {report_file}")
    print(f"\n📁 Tous les résultats sont dans: {output_path}/")


def main():
    """Fonction principale"""
    print("=" * 80)
    print("🐢 Giskard RAGET - Évaluation du chat Diplomeo dev")
    print("=" * 80)
    print(f"Ragflow Host: {RAGFLOW_HOST}")
    print(f"Chat ID: {CHAT_ID}")
    print(f"Base de connaissances: ragflow-sample/")
    print("=" * 80)
    
    # Vérifier la variable d'environnement OpenAI
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  ATTENTION: La variable OPENAI_API_KEY n'est pas définie")
        print("   RAGET nécessite un LLM pour générer les questions/réponses")
        print("   Configurez: export OPENAI_API_KEY='votre-clé'")
        user_continue = input("\n   Continuer quand même? [o/N]: ")
        if user_continue.lower() != 'o':
            return
    
    # 1. Initialiser l'agent Ragflow (chat Diplomeo dev)
    print("\n1️⃣  Initialisation du chat Diplomeo dev...")
    agent = RagflowAgent(RAGFLOW_HOST, RAGFLOW_API_KEY, CHAT_ID)
    
    # Test rapide
    test_question = "Quelles formations en informatique sont disponibles?"
    print(f"   Test: '{test_question}'")
    test_result = agent.query(test_question)
    print(f"   ✓ Réponse reçue ({len(test_result['answer'])} caractères)")
    
    # 2. Charger la base de connaissances depuis ragflow-sample/
    print("\n2️⃣  Chargement de la base de connaissances depuis ragflow-sample/...")
    knowledge_base = load_knowledge_base_from_ragflow_sample()
    
    if knowledge_base.empty:
        print("❌ Aucun document chargé depuis ragflow-sample/")
        return
    
    # 3. Générer le testset avec RAGET
    print("\n3️⃣  Génération du testset avec RAGET...")
    num_questions = input("   Nombre de questions à générer [défaut: 20]: ").strip()
    num_questions = int(num_questions) if num_questions else 20
    
    testset = generate_testset_with_raget(knowledge_base, num_questions=num_questions)
    
    if testset is None:
        print("❌ Impossible de générer le testset")
        return
    
    # 4. Évaluer le chat Diplomeo dev
    print("\n4️⃣  Évaluation du chat Diplomeo dev...")
    results_df = evaluate_rag_with_testset(agent, testset)
    
    # 5. Analyser les résultats
    print("\n5️⃣  Analyse des résultats...")
    stats = analyze_results(results_df)
    
    # 6. Sauvegarder les résultats
    print("\n6️⃣  Sauvegarde des résultats...")
    save_results(testset, results_df, stats)
    
    print("\n" + "=" * 80)
    print("✅ Évaluation terminée avec succès!")
    print("=" * 80)
    print("\n💡 Prochaines étapes:")
    print("   - Consultez le rapport dans giskard_results/")
    print("   - Analysez les questions/réponses dans le fichier CSV")
    print("   - Utilisez le testset pour améliorer le prompt ou les données")


if __name__ == "__main__":
    main()
