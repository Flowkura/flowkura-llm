# 🚀 Convertisseur XML → Markdown ONISEP/IDEO

**Un seul script** pour convertir tous les fichiers XML ONISEP/IDEO en Markdown optimisé pour RagFlow.

## ⚡ Démarrage rapide

```bash
# 1. Installation
mise use python@3.11 uv

# 2. Conversion COMPLÈTE
./convert_all.sh

# C'est tout ! ~10,000 fichiers Markdown dans output/
```

## 📦 Ce qui est converti

✅ **Fiches ONISEP détaillées** (2,342 formations + 1,043 métiers)  
✅ **Référentiels IDEO** (5,776 formations + 1,489 métiers)  
✅ **Actions de formation** (collège, lycée, supérieur)  
✅ **Autres données** (dispositifs, spécialités, langues, structures, etc.)

**Total:** ~10,000+ fichiers Markdown à partir de 14 fichiers XML (~269 MB)

## 🎯 Utilisation

### Tout convertir (recommandé)

```bash
./convert_all.sh
```

### Conversion sélective

```bash
# Fiches ONISEP détaillées
python convert_xml_to_markdown.py formations_onisep metiers_onisep

# Référentiels IDEO
python convert_xml_to_markdown.py formations_ideo metiers_ideo

# Voir toutes les options
python convert_xml_to_markdown.py --help
```

## 🛠️ Utilitaires

```bash
python generate_stats.py          # Statistiques
python search.py "informatique"   # Recherche
python validate.py                # Validation qualité
./view.sh FOR.1000                # Afficher un fichier
```

## 📁 Structure de sortie

```
output/
├── formations/                # Fiches formations ONISEP
├── metiers/                   # Fiches métiers ONISEP
├── ideo_formations/           # Référentiel formations
├── ideo_metiers/              # Référentiel métiers
└── ideo_*/                    # Autres données (10 dossiers)
```

## ✨ Avantages

- ✅ **Un seul script** pour tout
- ✅ **Pas de dépendances** externes
- ✅ **Rapide** : 5-10 min pour tout
- ✅ **Qualité** : 90-95% de validité
- ✅ **Prêt RagFlow** : Markdown optimisé

## 📊 Fichiers du projet

| Fichier | Description |
|---------|-------------|
| `convert_xml_to_markdown.py` | ⭐ Script principal unique |
| `convert_all.sh` | Raccourci bash |
| `generate_stats.py` | Statistiques |
| `search.py` | Recherche par mots-clés |
| `validate.py` | Validation qualité |
| `view.sh` | Affichage rapide |

## 🔍 Recherche et exploration

```bash
# Rechercher
python search.py "développeur web"

# Afficher
./view.sh FOR.1000

# Statistiques
python generate_stats.py

# Valider
python validate.py
```

## 💡 Exemples

```bash
# Tout convertir
./convert_all.sh

# Seulement ONISEP détaillé
python convert_xml_to_markdown.py formations_onisep metiers_onisep

# Seulement référentiels IDEO
python convert_xml_to_markdown.py formations_ideo metiers_ideo

# Actions de formation
python convert_xml_to_markdown.py actions

# Voir les options
python convert_xml_to_markdown.py --help
```

## ⏱️ Performance

- **Tout** : ~5-10 minutes → ~10,000+ fichiers
- **ONISEP** : ~45 secondes → 3,385 fichiers
- **IDEO** : ~2 minutes → ~7,000+ fichiers

## 🔧 Configuration

- Python 3.11+ (via mise)
- RAM : 2-4 GB
- Disque : 500 MB libres
- Dépendances : **Aucune** (stdlib seulement)

---

**🎯 100% prêt pour RagFlow !**
