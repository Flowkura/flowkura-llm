# Évaluation du RAG Flowkura avec Giskard RAGET

Ce document explique comment évaluer le chat **Diplomeo dev** sur Ragflow en utilisant **Giskard RAGET** pour générer automatiquement un testset de questions/réponses.

## 🎯 Objectif

Générer automatiquement un **testset d'évaluation** à partir de la base de connaissances `ragflow-sample/` et l'utiliser pour tester le chat Diplomeo dev de manière systématique.

## 📦 Prérequis

### 1. Installation de Giskard

```bash
# Installation (peut prendre 5-10 minutes, télécharge ~1GB de dépendances)
pip install -r requirements-giskard.txt
```

**Note**: Giskard installe PyTorch et de nombreuses dépendances ML. Si vous avez déjà PyTorch installé, vous pouvez installer uniquement :
```bash
pip install giskard
```

### 2. Configuration OpenAI

RAGET utilise un LLM pour générer les questions/réponses. Vous devez configurer votre clé API OpenAI :

```bash
export OPENAI_API_KEY='votre-clé-openai'
```

Vous pouvez aussi utiliser d'autres LLMs supportés par Giskard (Anthropic Claude, Mistral, etc.).

## 🚀 Utilisation

### Script principal : `giskard_raget_evaluation.py`

```bash
python giskard_raget_evaluation.py
```

Le script va :

1. **Se connecter au chat Diplomeo dev** sur Ragflow
2. **Charger la base de connaissances** depuis `ragflow-sample/` :
   - `1_metiers/` : 9 fiches métiers
   - `2_formations/` : 12 formations
   - `3_actions_formation/` : 41 actions de formation
   - `4_etablissements/` : Établissements
3. **Générer un testset avec RAGET** (20 questions par défaut)
4. **Évaluer le chat** en lui posant toutes les questions
5. **Analyser les résultats** et générer un rapport

### Résultats

Tous les résultats sont sauvegardés dans `giskard_results/` :

```
giskard_results/
├── testset_20260204_HHMMSS.jsonl          # Testset réutilisable
├── evaluation_results_20260204_HHMMSS.csv # Résultats détaillés
├── stats_20260204_HHMMSS.json             # Statistiques
└── report_20260204_HHMMSS.md              # Rapport Markdown
```

## 📊 Que fait RAGET ?

**RAGET** (RAG Evaluation Toolkit) de Giskard génère automatiquement différents types de questions :

### Types de questions générées

1. **Questions simples** : Questions directes sur le contenu
   - Exemple : "Quels sont les prérequis pour le BTS Comptabilité ?"

2. **Questions complexes** : Questions nécessitant plusieurs sources
   - Exemple : "Quelles formations en comptabilité sont disponibles à Lille ?"

3. **Questions de distracteurs** : Questions avec des informations trompeuses
   - Exemple : "Le BTS Informatique est-il disponible en 1 an ?" (Faux)

4. **Questions conversationnelles** : Questions avec contexte
   - Exemple : "Je cherche une formation. → En comptabilité. → À Lille."

5. **Questions hors contexte** : Questions sans réponse dans la base
   - Exemple : "Quel est le salaire moyen d'un comptable ?" (Si non documenté)

## 🎨 Personnalisation

### Modifier le nombre de questions

Éditez le script ou passez le paramètre :

```python
num_questions = 50  # Au lieu de 20
```

### Changer le LLM utilisé

Par défaut, RAGET utilise OpenAI GPT-4. Pour utiliser un autre modèle :

```python
from giskard.llm import set_default_client
from giskard.llm.client import OpenAIClient

# Utiliser GPT-3.5 au lieu de GPT-4 (moins cher)
client = OpenAIClient(model="gpt-3.5-turbo")
set_default_client(client)
```

### Filtrer la base de connaissances

Pour ne tester que certaines catégories :

```python
# Ne charger que les formations et métiers
knowledge_base = knowledge_base[
    knowledge_base['category'].isin([
        'Formations - Orientation France',
        'Métiers - Orientation France'
    ])
]
```

## 📈 Métriques et analyse

Le script génère plusieurs métriques :

### Métriques basiques

- **Total de questions** : Nombre total de questions testées
- **Longueur moyenne des réponses** : En caractères
- **Réponses vides** : Nombre de fois où le RAG n'a pas répondu
- **Réponses avec erreur** : Réponses contenant "erreur"

### Métriques avancées (si activé)

Pour activer les métriques RAGET avancées, décommentez la section dans le script :

```python
# Calculer les métriques RAGET
from giskard.rag import evaluate

metrics = evaluate(
    question=results_df['question'],
    reference_answer=results_df['reference_answer'],
    answer=results_df['rag_answer'],
    reference_context=results_df['reference_context']
)
```

Ces métriques évaluent :
- **Generator** : Qualité des réponses générées
- **Retriever** : Pertinence des documents récupérés
- **Overall** : Score global du système RAG

## 🔧 Dépannage

### Erreur : "OPENAI_API_KEY not found"

```bash
export OPENAI_API_KEY='sk-...'
```

### Erreur : "ImportError: giskard"

```bash
pip install -r requirements-giskard.txt
```

### Installation trop longue

Giskard installe PyTorch (~1GB). C'est normal. L'installation peut prendre 5-10 minutes.

### Le testset ne se génère pas

- Vérifiez que `ragflow-sample/` contient bien des fichiers `.md`
- Vérifiez votre clé OpenAI
- Réduisez le nombre de questions pour tester

## 📚 Ressources

- [Documentation Giskard](https://docs.giskard.ai/)
- [RAGET - RAG Evaluation Toolkit](https://docs.giskard.ai/en/stable/open_source/scan/rag_evaluation/index.html)
- [GitHub Giskard](https://github.com/Giskard-AI/giskard-oss)

## 💡 Utilisation avancée

### Réutiliser un testset existant

```python
from giskard.rag import QATestset

# Charger un testset sauvegardé
testset = QATestset.load("giskard_results/testset_20260204_120000.jsonl")

# Évaluer à nouveau avec ce testset
results = evaluate_rag_with_testset(agent, testset)
```

### Ajouter des questions manuelles

```python
# Créer un testset personnalisé
custom_questions = [
    {
        "question": "Quelles formations en comptabilité à Lille ?",
        "reference_answer": "BTS Comptabilité et Gestion disponible à Lille",
        "reference_context": "...",
        "metadata": {"question_type": "custom"}
    }
]

# Combiner avec le testset RAGET
# ... (voir documentation Giskard)
```

## 🎯 Cas d'usage

### 1. Tester une nouvelle version du prompt

1. Générez un testset avec la version actuelle
2. Sauvegardez les résultats
3. Modifiez le prompt du chat
4. Re-testez avec le même testset
5. Comparez les résultats

### 2. Tester l'ajout de nouveaux documents

1. Testset initial avec les documents actuels
2. Ajoutez de nouveaux documents à Ragflow
3. Re-testez avec le même testset
4. Vérifiez si les réponses s'améliorent

### 3. Benchmarking continu

- Générez un testset de référence
- Testez régulièrement (après chaque modification)
- Suivez l'évolution des métriques dans le temps

## 📝 Structure du code

```
giskard_raget_evaluation.py
├── RagflowAgent                          # Wrapper pour le chat Diplomeo dev
│   ├── query()                           # Interroger le chat
│   └── get_answer()                      # Version simplifiée
├── load_knowledge_base_from_ragflow_sample()  # Charger ragflow-sample/
├── generate_testset_with_raget()         # Générer le testset
├── evaluate_rag_with_testset()           # Évaluer le RAG
├── analyze_results()                     # Analyser les résultats
├── save_results()                        # Sauvegarder tout
└── main()                                # Orchestration
```

---

**Bon test ! 🚀**
