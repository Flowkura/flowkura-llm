#!/bin/bash
# Script pour afficher rapidement un fichier par son ID

if [ $# -eq 0 ]; then
    echo "Usage: ./view.sh <ID>"
    echo ""
    echo "Exemples:"
    echo "  ./view.sh FOR.1000     # Voir une formation"
    echo "  ./view.sh MET.100      # Voir un métier"
    echo ""
    echo "Astuce: Utilisez search.py pour trouver les IDs"
    exit 1
fi

ID=$1

# Chercher dans les formations
FORMATION_FILE=$(find output/formations -name "${ID}_*.md" 2>/dev/null)

# Chercher dans les métiers
METIER_FILE=$(find output/metiers -name "${ID}_*.md" 2>/dev/null)

if [ -n "$FORMATION_FILE" ]; then
    echo "📚 Formation trouvée: $FORMATION_FILE"
    echo "========================================================================"
    cat "$FORMATION_FILE"
elif [ -n "$METIER_FILE" ]; then
    echo "💼 Métier trouvé: $METIER_FILE"
    echo "========================================================================"
    cat "$METIER_FILE"
else
    echo "❌ Aucun fichier trouvé avec l'ID: $ID"
    echo ""
    echo "Suggestions:"
    echo "  - Vérifiez l'orthographe de l'ID"
    echo "  - Utilisez: python search.py <mot-clé>"
    exit 1
fi
