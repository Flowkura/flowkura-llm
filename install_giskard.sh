#!/bin/bash
# Script d'installation simplifié pour Giskard RAGET
# Evite les dépendances CUDA lourdes en utilisant la version CPU-only

set -e

echo "🐢 Installation de Giskard pour l'évaluation RAGET"
echo "=================================================="
echo ""

# Vérifier si on est dans un environnement virtuel
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Vous n'êtes pas dans un environnement virtuel"
    echo "   Recommandé: créer un venv d'abord"
    echo ""
    read -p "   Continuer quand même? [o/N]: " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Oo]$ ]]; then
        exit 1
    fi
fi

# Installation minimale sans PyTorch lourd
echo "📦 Installation des dépendances de base..."
pip install --upgrade pip

echo ""
echo "📦 Installation de pandas et requests..."
pip install pandas>=2.0.0 requests>=2.19.0

echo ""
echo "📦 Installation de Giskard (version légère)..."
# Installer d'abord les dépendances sans les lourdes versions CUDA
pip install --no-deps giskard

echo ""
echo "📦 Installation des dépendances minimales de Giskard..."
pip install \
    cloudpickle>=1.1.1 \
    numpy==1.26.4 \
    scikit-learn>=1.0 \
    pydantic \
    jinja2 \
    pyyaml \
    requests \
    packaging \
    typing-extensions

echo ""
echo "📦 Installation de transformers et huggingface (pour RAGET)..."
pip install transformers>=4.0.0 huggingface-hub>=0.7.0 datasets>=2.0.0

echo ""
echo "📦 Installation d'OpenAI (pour GPT-4)..."
pip install openai>=1.0.0

echo ""
echo "✅ Installation terminée!"
echo ""
echo "📝 Prochaines étapes:"
echo "   1. Configurez votre clé OpenAI:"
echo "      export OPENAI_API_KEY='votre-clé'"
echo ""
echo "   2. Lancez le script d'évaluation:"
echo "      python giskard_raget_evaluation.py"
echo ""
echo "💡 Note: Si vous avez besoin des fonctionnalités complètes (scan, etc.),"
echo "   installez la version complète avec: pip install 'giskard[llm]'"
