#!/bin/bash

# Configuration
API_KEY="ragflow-d4iWypSjduSHlkWb-wFOwda57ytZFsE7sxc6npOt9b8"
SERVER="https://rag-staging.flowkura.com"
BASE_DIR="./ragflow-sample"

# Couleurs pour l'affichage
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "======================================================================"
echo "Upload des fichiers ragflow-sample vers RAGFlow"
echo "======================================================================"
echo ""

# Fonction pour créer un dataset
create_dataset() {
    local name="$1"
    local description="$2"
    
    echo "Création du dataset '$name'..."
    
    local response=$(curl -s -X POST \
        "$SERVER/api/v1/datasets" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $API_KEY" \
        -d "{
            \"name\": \"$name\",
            \"description\": \"$description\",
            \"embedding_model\": \"Snowflake/snowflake-arctic-embed-m-v2.0___VLLM@VLLM\",
            \"chunk_method\": \"naive\",
            \"parser_config\": {
                \"chunk_token_num\": 512,
                \"delimiter\": \"\\\\n\",
                \"auto_keywords\": 6,
                \"auto_questions\": 3,
                \"graphrag\": {
                    \"entity_types\": [\"organization\", \"person\", \"geo\", \"event\", \"category\"],
                    \"method\": \"light\",
                    \"use_graphrag\": true
                },
                \"raptor\": {
                    \"use_raptor\": true,
                    \"max_cluster\": 64,
                    \"max_token\": 256,
                    \"threshold\": 0.1,
                    \"random_seed\": 0,
                    \"prompt\": \"Please summarize the following paragraphs. Be careful with the numbers, do not make things up. Paragraphs as following:\\n      {cluster_content}\\nThe above is the content you need to summarize.\"
                }
            }
        }")
    
    # Vérifier si jq est disponible
    if command -v jq &> /dev/null; then
        local dataset_id=$(echo "$response" | jq -r '.data.id')
    else
        # Fallback sans jq
        local dataset_id=$(echo "$response" | sed -n 's/.*"id":"\([^"]*\)".*/\1/p' | head -1)
    fi
    
    if [ -n "$dataset_id" ] && [ "$dataset_id" != "null" ]; then
        echo -e "${GREEN}✓ Dataset créé avec succès - ID: $dataset_id${NC}"
        echo "$dataset_id"
        return 0
    else
        echo -e "${RED}✗ Erreur lors de la création du dataset${NC}"
        echo "Response: $response"
        return 1
    fi
}

# Fonction pour uploader les fichiers d'un dossier
upload_documents() {
    local dataset_id="$1"
    local folder_path="$2"
    local uploaded=0
    
    echo "Upload des fichiers depuis $folder_path..."
    
    for file in "$folder_path"/*.md; do
        if [ -f "$file" ]; then
            local filename=$(basename "$file")
            echo -n "  Upload: $filename... "
            
            local response=$(curl -s -X POST \
                "$SERVER/api/v1/datasets/$dataset_id/documents" \
                -H "Authorization: Bearer $API_KEY" \
                -F "file=@$file")
            
            if echo "$response" | grep -q '"code":0'; then
                echo -e "${GREEN}✓${NC}"
                ((uploaded++))
            else
                echo -e "${RED}✗${NC}"
            fi
            
            # Petit délai pour éviter de surcharger l'API
            sleep 0.2
        fi
    done
    
    echo "$uploaded"
}

# Fonction pour lancer le parsing des documents
parse_documents() {
    local dataset_id="$1"
    
    echo "Récupération de la liste des documents..."
    
    # Récupérer la liste des documents
    local docs_response=$(curl -s -X GET \
        "$SERVER/api/v1/datasets/$dataset_id/documents?page_size=1000" \
        -H "Authorization: Bearer $API_KEY")
    
    # Extraire les IDs des documents
    local doc_ids=$(echo "$docs_response" | grep -o '"id":"[^"]*"' | cut -d'"' -f4 | tr '\n' ',' | sed 's/,$//')
    
    if [ -z "$doc_ids" ]; then
        echo -e "${RED}✗ Aucun document trouvé${NC}"
        return 1
    fi
    
    # Convertir en tableau JSON
    local doc_ids_json=$(echo "$doc_ids" | sed 's/,/","/g' | sed 's/^/["/' | sed 's/$/"]/')
    
    echo "Lancement du parsing des documents..."
    
    local parse_response=$(curl -s -X POST \
        "$SERVER/api/v1/datasets/$dataset_id/chunks" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $API_KEY" \
        -d "{\"document_ids\": $doc_ids_json}")
    
    if echo "$parse_response" | grep -q '"code":0'; then
        echo -e "${GREEN}✓ Parsing lancé avec succès${NC}"
        return 0
    else
        echo -e "${RED}✗ Erreur lors du lancement du parsing${NC}"
        echo "Response: $parse_response"
        return 1
    fi
}

# Vérifier que le dossier existe
if [ ! -d "$BASE_DIR" ]; then
    echo -e "${RED}✗ Erreur: Le dossier $BASE_DIR n'existe pas${NC}"
    exit 1
fi

total_uploaded=0

# Dataset 1: Métiers
echo ""
echo "======================================================================"
echo "Traitement du dossier: 1_metiers"
echo "======================================================================"

dataset_id=$(create_dataset \
    "Métiers - Orientation France" \
    "Fiches métiers détaillées avec variantes de genre pour la recherche inclusive. Contient 9 métiers avec codes ROME et variantes masculin/féminin.")

if [ $? -eq 0 ] && [ -n "$dataset_id" ]; then
    sleep 1
    uploaded=$(upload_documents "$dataset_id" "$BASE_DIR/1_metiers")
    total_uploaded=$((total_uploaded + uploaded))
    echo -e "\n${GREEN}✓ $uploaded fichiers uploadés pour 1_metiers${NC}"
    sleep 2
    parse_documents "$dataset_id"
    sleep 5
fi

# Dataset 2: Formations
echo ""
echo "======================================================================"
echo "Traitement du dossier: 2_formations"
echo "======================================================================"

dataset_id=$(create_dataset \
    "Formations - Orientation France" \
    "Programmes et diplômes du Bac au Bac+3. Contient 12 formations (Bac général, Bac pro, BTS, Diplômes d'État) avec niveaux et types de formation.")

if [ $? -eq 0 ] && [ -n "$dataset_id" ]; then
    sleep 1
    uploaded=$(upload_documents "$dataset_id" "$BASE_DIR/2_formations")
    total_uploaded=$((total_uploaded + uploaded))
    echo -e "\n${GREEN}✓ $uploaded fichiers uploadés pour 2_formations${NC}"
    sleep 2
    parse_documents "$dataset_id"
    sleep 5
fi

# Dataset 3: Actions de formation
echo ""
echo "======================================================================"
echo "Traitement du dossier: 3_actions_formation"
echo "======================================================================"

dataset_id=$(create_dataset \
    "Actions de Formation - Orientation France" \
    "Actions concrètes avec lieux, dates et modalités. Contient 120 actions de formation avec géolocalisation GPS, régions, statut public/privé et durée.")

if [ $? -eq 0 ] && [ -n "$dataset_id" ]; then
    sleep 1
    uploaded=$(upload_documents "$dataset_id" "$BASE_DIR/3_actions_formation")
    total_uploaded=$((total_uploaded + uploaded))
    echo -e "\n${GREEN}✓ $uploaded fichiers uploadés pour 3_actions_formation${NC}"
    sleep 2
    parse_documents "$dataset_id"
    sleep 5
fi

# Dataset 4: Établissements
echo ""
echo "======================================================================"
echo "Traitement du dossier: 4_etablissements"
echo "======================================================================"

dataset_id=$(create_dataset \
    "Établissements - Orientation France" \
    "Lieux d'enseignement avec adresses et coordonnées GPS. Contient 119 établissements avec codes UAI, coordonnées exactes, accessibilité et contact.")

if [ $? -eq 0 ] && [ -n "$dataset_id" ]; then
    sleep 1
    uploaded=$(upload_documents "$dataset_id" "$BASE_DIR/4_etablissements")
    total_uploaded=$((total_uploaded + uploaded))
    echo -e "\n${GREEN}✓ $uploaded fichiers uploadés pour 4_etablissements${NC}"
    sleep 2
    parse_documents "$dataset_id"
fi

echo ""
echo "======================================================================"
echo -e "${GREEN}✓ Upload terminé!${NC}"
echo "Total de fichiers uploadés: $total_uploaded"
echo "======================================================================"
