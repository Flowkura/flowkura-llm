# 🐢 Installation et configuration de Giskard RAGET pour Flowkura

## ✅ Fichiers créés

J'ai créé les fichiers suivants pour l'évaluation de votre RAG avec Giskard :

### 1. Script principal
- **`giskard_raget_evaluation.py`** : Script d'évaluation complet qui :
  - Charge la base de connaissances depuis `ragflow-sample/`
  - Génère un testset automatique avec RAGET
  - Teste le chat Diplomeo dev sur Ragflow
  - Analyse et sauvegarde les résultats

### 2. Documentation
- **`GISKARD_RAGET_README.md`** : Guide complet d'utilisation avec exemples

### 3. Installation
- **`requirements-giskard.txt`** : Liste des dépendances Python
- **`install_giskard.sh`** : Script d'installation optimisé (évite les dépendances CUDA lourdes)

## 🚀 Comment utiliser

### Étape 1 : Installation

**Option A - Installation rapide (recommandée)** :
```bash
./install_giskard.sh
```

**Option B - Installation complète** (prend 5-10 minutes, télécharge ~1GB) :
```bash
pip install -r requirements-giskard.txt
```

**Note importante** : L'installation de `giskard[llm]` inclut PyTorch avec support CUDA (~915 MB). C'est normal et nécessaire pour les fonctionnalités avancées. Si vous avez des problèmes d'espace disque, utilisez le script `install_giskard.sh` qui installe uniquement les dépendances minimales.

### Étape 2 : Configuration OpenAI

RAGET a besoin d'un LLM pour générer les questions/réponses. Configurez votre clé OpenAI :

```bash
export OPENAI_API_KEY='sk-votre-clé-openai'
```

Vous pouvez aussi utiliser un fichier `.env` :
```bash
echo "OPENAI_API_KEY=sk-votre-clé" >> .env
```

### Étape 3 : Lancer l'évaluation

```bash
python giskard_raget_evaluation.py
```

Le script va :
1. Se connecter au chat **Diplomeo dev** sur Ragflow
2. Charger les **62 documents** de `ragflow-sample/` :
   - 9 métiers
   - 12 formations
   - 41 actions de formation
3. Générer **20 questions** automatiques (vous pouvez modifier ce nombre)
4. Tester le chat avec ces questions
5. Générer un rapport dans `giskard_results/`

### Étape 4 : Consulter les résultats

```bash
ls -lh giskard_results/
```

Vous trouverez :
- `testset_*.jsonl` : Le testset généré (réutilisable)
- `evaluation_results_*.csv` : Résultats détaillés question/réponse
- `stats_*.json` : Statistiques globales
- `report_*.md` : Rapport Markdown lisible

## 📊 Ce que RAGET génère

RAGET crée automatiquement différents types de questions :

1. **Questions simples** : "Quels sont les prérequis pour le BTS Comptabilité ?"
2. **Questions complexes** : "Quelles formations en informatique sont disponibles à Lille ?"
3. **Questions avec distracteurs** : "Le BTS Informatique dure 1 an ?" (faux)
4. **Questions conversationnelles** : Avec historique de conversation
5. **Questions hors contexte** : Pour tester comment le RAG gère l'inconnu

## 🎯 Cas d'usage

### 1. Tester un nouveau prompt
```bash
# 1. Générer le testset de référence
python giskard_raget_evaluation.py  # Sauvegarder le testset

# 2. Modifier le prompt sur Ragflow

# 3. Re-tester avec le même testset
# (modifier le script pour charger le testset existant)

# 4. Comparer les résultats
```

### 2. Valider l'ajout de documents
- Tester avant/après l'ajout de nouveaux documents
- Vérifier que les réponses s'améliorent

### 3. Benchmarking continu
- Générer un testset de référence
- Re-tester après chaque modification
- Suivre l'évolution des métriques

## 🔧 Personnalisation

### Modifier le nombre de questions

Dans `giskard_raget_evaluation.py`, ligne ~361 :
```python
num_questions = int(num_questions) if num_questions else 20  # Changer 20
```

### Filtrer les catégories testées

Dans la fonction `load_knowledge_base_from_ragflow_sample()`, commentez les catégories non désirées :
```python
folders = {
    "1_metiers": "Métiers - Orientation France",
    "2_formations": "Formations - Orientation France", 
    # "3_actions_formation": "Actions de Formation - Orientation France",  # Désactivé
}
```

### Utiliser un autre LLM

Au début du script, ajoutez :
```python
from giskard.llm import set_default_client
from giskard.llm.client import OpenAIClient

# Utiliser GPT-3.5 au lieu de GPT-4 (moins cher)
client = OpenAIClient(model="gpt-3.5-turbo")
set_default_client(client)
```

## ⚠️ Points d'attention

### 1. Installation longue
L'installation de Giskard prend du temps car elle inclut PyTorch (~1GB). C'est normal. Utilisez `install_giskard.sh` pour une version plus légère.

### 2. Coûts OpenAI
RAGET fait de nombreux appels à l'API OpenAI. Pour 20 questions :
- Avec GPT-4 : ~$1-2
- Avec GPT-3.5 : ~$0.10-0.20

### 3. Temps d'exécution
La génération du testset peut prendre :
- 5-10 minutes pour 20 questions
- 20-30 minutes pour 50 questions

### 4. Variables d'environnement
Les credentials Ragflow sont dans le script. Pour plus de sécurité :
```bash
export RAGFLOW_API_KEY="votre-clé"
export OPENAI_API_KEY="votre-clé"
```

## 📚 Ressources

- [Documentation Giskard](https://docs.giskard.ai/)
- [RAGET Guide](https://docs.giskard.ai/en/stable/open_source/scan/rag_evaluation/index.html)
- [GitHub Giskard](https://github.com/Giskard-AI/giskard-oss)

## 🐛 Dépannage

### "Import pandas could not be resolved"
```bash
pip install pandas
```

### "Import giskard.rag could not be resolved"
```bash
pip install 'giskard[llm]'
```

### "OPENAI_API_KEY not found"
```bash
export OPENAI_API_KEY='sk-...'
```

### L'installation pip est trop longue
- Utilisez `install_giskard.sh` au lieu de pip install
- Ou installez en arrière-plan : `pip install 'giskard[llm]' &`

## 🎉 Prochaines étapes

1. **Installer** : `./install_giskard.sh`
2. **Configurer** : `export OPENAI_API_KEY='...'`
3. **Lancer** : `python giskard_raget_evaluation.py`
4. **Analyser** : Consultez `giskard_results/report_*.md`
5. **Itérer** : Modifiez le prompt, re-testez, comparez

---

**Besoin d'aide ?** Consultez `GISKARD_RAGET_README.md` pour plus de détails.
