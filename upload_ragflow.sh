#!/bin/bash

# Configuration
API_KEY="ragflow-d4iWypSjduSHlkWb-wFOwda57ytZFsE7sxc6npOt9b8"
SERVER="https://rag-staging.flowkura.com"
BASE_DIR="./ragflow-sample"

echo "======================================================================"
echo "Upload des fichiers ragflow-sample vers RAGFlow"
echo "======================================================================"

# Dataset 1: Métiers
echo ""
echo "=== 1. Création du dataset Métiers ==="
DATASET1=$(curl -s -X POST "$SERVER/api/v1/datasets" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "name": "Métiers",
    "description": "Fiches métiers détaillées avec variantes de genre pour la recherche inclusive. Contient 9 métiers avec codes ROME et variantes masculin/féminin.",
    "chunk_method": "naive",
    "parser_config": {
      "chunk_token_num": 512,
      "delimiter": "\n",
      "auto_keywords": 6,
      "auto_questions": 3,
      "graphrag": {"use_graphrag": true},
      "raptor": {"use_raptor": true}
    }
  }' | jq -r '.data.id')

echo "Dataset Métiers créé: $DATASET1"

echo "Upload des fichiers métiers..."
for file in $BASE_DIR/1_metiers/*.md; do
  echo "  - $(basename $file)"
  curl -s -X POST "$SERVER/api/v1/datasets/$DATASET1/documents" \
    -H "Authorization: Bearer $API_KEY" \
    -F "file=@$file" > /dev/null
  sleep 0.1
done

# Dataset 2: Formations
echo ""
echo "=== 2. Création du dataset Formations ==="
DATASET2=$(curl -s -X POST "$SERVER/api/v1/datasets" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "name": "Formations",
    "description": "Programmes et diplômes du Bac au Bac+3. Contient 12 formations (Bac général, Bac pro, BTS, Diplômes d État) avec niveaux et types de formation.",
    "chunk_method": "naive",
    "parser_config": {
      "chunk_token_num": 512,
      "delimiter": "\n",
      "auto_keywords": 6,
      "auto_questions": 3,
      "graphrag": {"use_graphrag": true},
      "raptor": {"use_raptor": true}
    }
  }' | jq -r '.data.id')

echo "Dataset Formations créé: $DATASET2"

echo "Upload des fichiers formations..."
for file in $BASE_DIR/2_formations/*.md; do
  echo "  - $(basename $file)"
  curl -s -X POST "$SERVER/api/v1/datasets/$DATASET2/documents" \
    -H "Authorization: Bearer $API_KEY" \
    -F "file=@$file" > /dev/null
  sleep 0.1
done

# Dataset 3: Actions de formation
echo ""
echo "=== 3. Création du dataset Actions de Formation ==="
DATASET3=$(curl -s -X POST "$SERVER/api/v1/datasets" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "name": "Actions de Formation",
    "description": "Actions concrètes avec lieux, dates et modalités. Contient 120 actions de formation avec géolocalisation GPS, régions, statut public/privé et durée.",
    "chunk_method": "naive",
    "parser_config": {
      "chunk_token_num": 512,
      "delimiter": "\n",
      "auto_keywords": 6,
      "auto_questions": 3,
      "graphrag": {"use_graphrag": true},
      "raptor": {"use_raptor": true}
    }
  }' | jq -r '.data.id')

echo "Dataset Actions de Formation créé: $DATASET3"

echo "Upload des fichiers actions de formation..."
count=0
for file in $BASE_DIR/3_actions_formation/*.md; do
  count=$((count+1))
  echo "  - $(basename $file) ($count/120)"
  curl -s -X POST "$SERVER/api/v1/datasets/$DATASET3/documents" \
    -H "Authorization: Bearer $API_KEY" \
    -F "file=@$file" > /dev/null
  sleep 0.1
done

# Dataset 4: Établissements
echo ""
echo "=== 4. Création du dataset Établissements ==="
DATASET4=$(curl -s -X POST "$SERVER/api/v1/datasets" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "name": "Établissements",
    "description": "Lieux d enseignement avec adresses et coordonnées GPS. Contient 119 établissements avec codes UAI, coordonnées exactes, accessibilité et contact.",
    "chunk_method": "naive",
    "parser_config": {
      "chunk_token_num": 512,
      "delimiter": "\n",
      "auto_keywords": 6,
      "auto_questions": 3,
      "graphrag": {"use_graphrag": true},
      "raptor": {"use_raptor": true}
    }
  }' | jq -r '.data.id')

echo "Dataset Établissements créé: $DATASET4"

echo "Upload des fichiers établissements..."
count=0
for file in $BASE_DIR/4_etablissements/*.md; do
  count=$((count+1))
  echo "  - $(basename $file) ($count/119)"
  curl -s -X POST "$SERVER/api/v1/datasets/$DATASET4/documents" \
    -H "Authorization: Bearer $API_KEY" \
    -F "file=@$file" > /dev/null
  sleep 0.1
done

echo ""
echo "======================================================================"
echo "✓ Upload terminé!"
echo "======================================================================"
echo "Dataset IDs créés:"
echo "  - Métiers: $DATASET1"
echo "  - Formations: $DATASET2"
echo "  - Actions de Formation: $DATASET3"
echo "  - Établissements: $DATASET4"
echo ""
echo "Maintenant, lancez le parsing des documents dans l'interface RAGFlow"
echo "ou via l'API avec les IDs ci-dessus."
