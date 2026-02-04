# 🚀 Quick Start - Giskard RAGET pour Flowkura

## Installation (5-10 minutes)

```bash
# Option 1 : Installation légère (recommandée)
./install_giskard.sh

# Option 2 : Installation complète (~1GB)
pip install -r requirements-giskard.txt
```

## Configuration

```bash
# Obligatoire : Clé OpenAI pour RAGET
export OPENAI_API_KEY='sk-votre-clé-openai'
```

## Utilisation

```bash
# Lancer l'évaluation
python giskard_raget_evaluation.py
```

Le script va :
1. ✅ Se connecter au chat **Diplomeo dev** sur Ragflow
2. ✅ Charger **62 documents** depuis `ragflow-sample/`
3. ✅ Générer **20 questions** automatiques avec RAGET
4. ✅ Tester le chat et analyser les réponses
5. ✅ Générer un rapport dans `giskard_results/`

## Résultats

```bash
ls giskard_results/
# testset_YYYYMMDD_HHMMSS.jsonl        # Testset réutilisable
# evaluation_results_YYYYMMDD_HHMMSS.csv  # Résultats détaillés
# stats_YYYYMMDD_HHMMSS.json          # Statistiques
# report_YYYYMMDD_HHMMSS.md           # Rapport Markdown
```

## Types de questions générées

1. **Simples** : "Quels sont les prérequis pour le BTS Comptabilité ?"
2. **Complexes** : "Quelles formations en informatique à Lille ?"
3. **Distracteurs** : "Le BTS Informatique dure 1 an ?" (Faux)
4. **Conversationnelles** : Questions avec historique
5. **Hors contexte** : Test des limites du RAG

## Personnalisation

### Modifier le nombre de questions

Quand le script vous le demande, entrez le nombre souhaité (défaut : 20).

### Utiliser GPT-3.5 au lieu de GPT-4 (moins cher)

Ajoutez au début de `giskard_raget_evaluation.py` :

```python
from giskard.llm import set_default_client
from giskard.llm.client import OpenAIClient

client = OpenAIClient(model="gpt-3.5-turbo")
set_default_client(client)
```

## Coûts estimés (OpenAI)

- **GPT-4** : ~$1-2 pour 20 questions
- **GPT-3.5** : ~$0.10-0.20 pour 20 questions

## Temps d'exécution

- **Installation** : 5-10 minutes
- **Génération testset** : 5-10 minutes (20 questions)
- **Évaluation** : 2-5 minutes (dépend du RAG)

## Fichiers créés

```
flowkura-llm/
├── giskard_raget_evaluation.py    # Script principal
├── requirements-giskard.txt       # Dépendances
├── install_giskard.sh             # Installation rapide
├── GISKARD_INSTALLATION.md        # Guide complet
├── GISKARD_RAGET_README.md        # Documentation détaillée
└── giskard_results/               # Résultats (créé automatiquement)
```

## Dépannage

### "pandas not found"
```bash
pip install pandas
```

### "giskard not found"
```bash
./install_giskard.sh
```

### "OPENAI_API_KEY not set"
```bash
export OPENAI_API_KEY='sk-...'
```

## Documentation complète

- 📖 **GISKARD_INSTALLATION.md** : Guide d'installation détaillé
- 📚 **GISKARD_RAGET_README.md** : Documentation complète avec exemples

## Support

- [Giskard Docs](https://docs.giskard.ai/)
- [RAGET Guide](https://docs.giskard.ai/en/stable/open_source/scan/rag_evaluation/)
- [GitHub](https://github.com/Giskard-AI/giskard-oss)

---

**Prêt à évaluer votre RAG ! 🎉**
