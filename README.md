# 🚀 Convertisseur XML → Markdown ONISEP/IDEO

**Un seul script** pour convertir tous les fichiers XML ONISEP/IDEO en Markdown optimisé pour RagFlow.  
**Configuration externalisée** dans `config.toml` pour faciliter la personnalisation.

## ⚡ Démarrage rapide

```bash
# 1. Cloner le repo
git clone git@github.com:clifinger/onisep-xml-to-markdown.git
cd onisep-xml-to-markdown

# 2. Installation
mise use python@3.11 uv

# 3. Conversion COMPLÈTE (15 secondes)
./convert_all.sh

# Résultat: ~154,000 fichiers Markdown dans output/
```

> ⚠️ **Note:** Le dossier `output/` n'est pas inclus dans le repo GitHub.  
> Les fichiers Markdown sont générés localement en 15 secondes avec `./convert_all.sh`

## 📦 Ce qui est converti

✅ **Fiches ONISEP détaillées** (2,342 formations + 1,043 métiers)  
✅ **Référentiels IDEO** (5,776 formations + 1,489 métiers)  
✅ **Actions de formation** (79,027 actions: collège, lycée, supérieur)  
✅ **Autres données** (40,500+ : dispositifs, spécialités, langues, structures, etc.)

**Total:** ~154,000 fichiers Markdown à partir de 16 fichiers XML (~269 MB)

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

# Actions de formation avec fichiers découpés (gestion automatique)
python convert_xml_to_markdown.py actions_lycee actions_superieur

# Voir toutes les options
python convert_xml_to_markdown.py --help
```

## 📝 Configuration (config.toml)

La configuration est externalisée pour faciliter les modifications :

```toml
[conversions.formations_onisep]
file = "files/Onisep_Ideo_Fiches_Formations_21102025.xml"
output = "output/formations"
type = "formations_detaillees"
description = "Fiches formations ONISEP détaillées"

# Support des wildcards pour fichiers découpés
[conversions.actions_lycee]
file = "files/ideo-actions_de_formation_initiale-univers_lycee_part*.xml"
output = "output/ideo_actions_lycee"
type = "generic"
description = "Actions formation lycée"
```

**Avantages:**
- 📝 Facile à modifier sans toucher au code
- 📦 Support wildcards pour fichiers découpés
- 📖 Bien documenté avec commentaires
- ✨ Ajouter de nouveaux fichiers sans coder

## 🔪 Découpage des gros fichiers (> 50MB)

GitHub recommande des fichiers < 50MB. Le script `split_large_xml.py` découpe automatiquement :

```bash
python split_large_xml.py
```

**Résultat:**
- ✅ Fichiers découpés en parties < 50MB
- ✅ Chaque partie est un XML valide
- ✅ Conversion transparente (fusion automatique)

## 🛠️ Utilitaires

```bash
python detect_files.py            # ⭐ Détecter nouveaux fichiers + suggestions config
python split_large_xml.py         # Découper gros XML > 50MB
python generate_stats.py          # Statistiques
python search.py "informatique"   # Recherche
python validate.py                # Validation qualité
./view.sh FOR.1000                # Afficher un fichier
```

## 📁 Structure de sortie

```
output/
├── formations/                # Fiches formations ONISEP (2,342)
├── metiers/                   # Fiches métiers ONISEP (1,043)
├── ideo_formations/           # Référentiel formations (5,776)
├── ideo_metiers/              # Référentiel métiers (1,489)
├── ideo_actions_college/      # Actions collège (8,349)
├── ideo_actions_lycee/        # Actions lycée (42,123)
├── ideo_actions_superieur/    # Actions supérieur (28,555)
├── ideo_dispositifs/          # Dispositifs (23,160)
├── ideo_specialites_premiere/ # Spécialités 1ère (2,449)
├── ideo_optionnels_seconde/   # Optionnels 2nde (2,678)
├── ideo_langues/              # Langues collège (7,138)
├── ideo_structures_secondaire/# Établissements (15,264)
├── ideo_structures_superieur/ # Établissements sup (9,009)
└── ideo_certifications/       # Certifications (4,902)

TOTAL: ~154,000 fichiers
```

## ✨ Fonctionnalités

- ✅ **Config externalisée** (config.toml)
- ✅ **Support fichiers découpés** (wildcards)
- ✅ **Pas de dépendances** externes (stdlib seulement)
- ✅ **Rapide** : 15 secondes pour tout
- ✅ **Qualité** : Markdown propre et structuré
- ✅ **Prêt RagFlow** : Format optimisé

## 📊 Fichiers du projet

| Fichier | Description |
|---------|-------------|
| `config.toml` | ⭐ Configuration |
| `convert_xml_to_markdown.py` | Script principal |
| `detect_files.py` | 🆕 Détection auto + suggestions |
| `split_large_xml.py` | Découpage fichiers > 50MB |
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

## 💡 Personnalisation

### Ajouter un nouveau fichier XML

1. Éditer `config.toml`
2. Ajouter une nouvelle section
3. Relancer la conversion

```toml
[conversions.mon_nouveau_fichier]
file = "files/mon_fichier.xml"
output = "output/mon_output"
type = "generic"
description = "Ma description"
```

### Fichiers découpés

Si votre fichier est > 50MB :

```bash
# 1. Découper
python split_large_xml.py

# 2. Mettre à jour config.toml avec wildcard
file = "files/mon_fichier_part*.xml"

# 3. Convertir normalement
./convert_all.sh
```

## ⏱️ Performance

- **Tout** : ~15 secondes → ~154,000 fichiers
- **ONISEP** : ~1 seconde → 3,385 fichiers
- **IDEO** : ~14 secondes → ~150,000 fichiers

## 🔧 Configuration requise

- Python 3.11+ (via mise)
- RAM : 2-4 GB
- Disque : 500 MB libres
- Dépendances : **Aucune** (stdlib seulement)

## 🎯 Conformité GitHub

- ✅ Tous fichiers < 50 MB
- ✅ 0 avertissement
- ✅ Repo < 500 MB
- ✅ Format optimisé

---

**🎯 100% prêt pour RagFlow !**  
**Version:** 3.0 - Configuration externalisée + Support fichiers découpés

## 🔍 Détection automatique des fichiers

Le script `detect_files.py` détecte automatiquement les nouveaux fichiers XML et suggère leur configuration :

```bash
python detect_files.py
```

**Fonctionnalités:**
- ✅ Détecte les nouveaux fichiers dans `files/`
- ✅ Analyse leur structure (taille, items, tags)
- ✅ Suggère la configuration TOML complète
- ✅ Détecte les fichiers découpés (part*)
- ✅ Donne des conseils (taille > 50MB, beaucoup d'items, etc.)
- ✅ Tracking avec base SQLite locale

**Exemple de sortie:**

```
📄 mon_nouveau_fichier.xml
   Taille: 65.2 MB
   Items: 45,000

   💡 Notes:
   ⚠️  Fichier > 50MB (65.2 MB)
      → Lancer: python split_large_xml.py
      → Puis utiliser wildcard: files/mon_nouveau_fichier_part*.xml
   ℹ️  Beaucoup d'items (45,000)
      → Conversion peut prendre du temps

   📝 Configuration suggérée:

   [conversions.mon_fichier]
   file = "files/mon_nouveau_fichier.xml"
   output = "output/mon_fichier"
   type = "generic"
   description = "Mon fichier"
```

**Workflow pour un nouveau fichier:**

1. Copier le nouveau fichier XML dans `files/`
2. Lancer `python detect_files.py`
3. Copier la configuration suggérée dans `config.toml`
4. Si fichier > 50MB: `python split_large_xml.py`
5. Mettre à jour le pattern dans config.toml (wildcard)
6. Lancer `./convert_all.sh`
7. Marquer comme configuré: `python detect_files.py --mark-configured`
