#!/usr/bin/env python3
"""
Script pour uploader les fichiers du dossier ragflow-sample vers l'instance RAGFlow
"""

import os
import requests
import json
import time
from pathlib import Path
from typing import Dict, List

# Configuration
RAGFLOW_API_KEY = "ragflow-d4iWypSjduSHlkWb-wFOwda57ytZFsE7sxc6npOt9b8"
RAGFLOW_SERVER = "https://rag-staging.flowkura.com"
BASE_DIR = Path(__file__).parent / "ragflow-sample"

# Configuration basée sur le dataset "julien" existant
DATASET_CONFIG = {
    "embedding_model": "Snowflake/snowflake-arctic-embed-m-v2.0___VLLM@VLLM",
    "language": "French",
    "chunk_method": "naive",
    "parser_config": {
        "chunk_token_num": 512,
        "delimiter": "\\n",
        "auto_keywords": 6,
        "auto_questions": 3,
        "enable_metadata": True,
        "graphrag": {
            "entity_types": ["organization", "person", "geo", "event", "category"],
            "method": "light",
            "use_graphrag": True
        },
        "raptor": {
            "use_raptor": True,
            "max_cluster": 64,
            "max_token": 256,
            "threshold": 0.1,
            "random_seed": 0,
            "prompt": "Please summarize the following paragraphs. Be careful with the numbers, do not make things up. Paragraphs as following:\n      {cluster_content}\nThe above is the content you need to summarize.",
            "scope": "file"
        }
    },
    "similarity_threshold": 0.2,
    "vector_similarity_weight": 0.3
}

# Descriptions des datasets selon le README
DATASETS = {
    "1_metiers": {
        "name": "Métiers - Orientation France",
        "description": "Fiches métiers détaillées avec variantes de genre pour la recherche inclusive. Contient 9 métiers avec codes ROME et variantes masculin/féminin."
    },
    "2_formations": {
        "name": "Formations - Orientation France",
        "description": "Programmes et diplômes du Bac au Bac+3. Contient 12 formations (Bac général, Bac pro, BTS, Diplômes d'État) avec niveaux et types de formation."
    },
    "3_actions_formation": {
        "name": "Actions de Formation - Orientation France",
        "description": "Actions concrètes avec lieux, dates et modalités. Contient 120 actions de formation avec géolocalisation GPS, régions, statut public/privé et durée."
    },
    "4_etablissements": {
        "name": "Établissements - Orientation France",
        "description": "Lieux d'enseignement avec adresses et coordonnées GPS. Contient 119 établissements avec codes UAI, coordonnées exactes, accessibilité et contact."
    }
}


def create_dataset(name: str, description: str) -> str | None:
    """Crée un dataset dans RAGFlow"""
    url = f"{RAGFLOW_SERVER}/api/v1/datasets"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {RAGFLOW_API_KEY}"
    }
    
    data = {
        "name": name,
        "description": description,
        **DATASET_CONFIG
    }
    
    print(f"Création du dataset '{name}'...")
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == 0:
            dataset_id = result["data"]["id"]
            print(f"✓ Dataset créé avec succès - ID: {dataset_id}")
            return dataset_id
        else:
            print(f"✗ Erreur API: {result.get('message')}")
            return None
    else:
        print(f"✗ Erreur HTTP {response.status_code}: {response.text}")
        return None


def upload_documents(dataset_id: str, folder_path: Path) -> int:
    """Upload tous les fichiers markdown d'un dossier vers un dataset"""
    url = f"{RAGFLOW_SERVER}/api/v1/datasets/{dataset_id}/documents"
    headers = {
        "Authorization": f"Bearer {RAGFLOW_API_KEY}"
    }
    
    # Récupérer tous les fichiers .md
    md_files = list(folder_path.glob("*.md"))
    print(f"Trouvé {len(md_files)} fichiers à uploader...")
    
    uploaded_count = 0
    failed_count = 0
    
    for md_file in md_files:
        try:
            with open(md_file, 'rb') as f:
                files = {'file': (md_file.name, f, 'text/markdown')}
                print(f"  Upload: {md_file.name}...", end=" ")
                
                response = requests.post(url, headers=headers, files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("code") == 0:
                        print("✓")
                        uploaded_count += 1
                    else:
                        print(f"✗ Erreur: {result.get('message')}")
                        failed_count += 1
                else:
                    print(f"✗ HTTP {response.status_code}")
                    failed_count += 1
                
                # Petit délai pour éviter de surcharger l'API
                time.sleep(0.2)
                
        except Exception as e:
            print(f"✗ Exception: {e}")
            failed_count += 1
    
    return uploaded_count


def parse_documents(dataset_id: str) -> bool:
    """Lance le parsing des documents d'un dataset"""
    # Récupérer la liste des documents
    url = f"{RAGFLOW_SERVER}/api/v1/datasets/{dataset_id}/documents"
    headers = {
        "Authorization": f"Bearer {RAGFLOW_API_KEY}"
    }
    
    print("Récupération de la liste des documents...")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"✗ Erreur lors de la récupération des documents: {response.status_code}")
        return False
    
    result = response.json()
    if result.get("code") != 0:
        print(f"✗ Erreur API: {result.get('message')}")
        return False
    
    docs = result.get("data", {}).get("docs", [])
    document_ids = [doc["id"] for doc in docs]
    
    if not document_ids:
        print("✗ Aucun document trouvé")
        return False
    
    print(f"Lancement du parsing de {len(document_ids)} documents...")
    
    # Lancer le parsing
    parse_url = f"{RAGFLOW_SERVER}/api/v1/datasets/{dataset_id}/chunks"
    parse_data = {"document_ids": document_ids}
    
    response = requests.post(parse_url, headers=headers, json=parse_data)
    
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == 0:
            print("✓ Parsing lancé avec succès")
            return True
        else:
            print(f"✗ Erreur API: {result.get('message')}")
            return False
    else:
        print(f"✗ Erreur HTTP {response.status_code}: {response.text}")
        return False


def main():
    """Fonction principale"""
    print("=" * 70)
    print("Upload des fichiers ragflow-sample vers RAGFlow")
    print("=" * 70)
    print()
    
    # Vérifier que le dossier ragflow-sample existe
    if not BASE_DIR.exists():
        print(f"✗ Erreur: Le dossier {BASE_DIR} n'existe pas")
        return
    
    total_uploaded = 0
    
    # Traiter chaque dossier
    for folder_name, config in DATASETS.items():
        folder_path = BASE_DIR / folder_name
        
        if not folder_path.exists():
            print(f"⚠ Dossier {folder_name} non trouvé, passage au suivant")
            continue
        
        print(f"\n{'=' * 70}")
        print(f"Traitement du dossier: {folder_name}")
        print(f"{'=' * 70}")
        
        # Créer le dataset
        dataset_id = create_dataset(config["name"], config["description"])
        
        if not dataset_id:
            print(f"✗ Impossible de créer le dataset pour {folder_name}")
            continue
        
        # Attendre un peu après la création du dataset
        time.sleep(1)
        
        # Upload des fichiers
        uploaded = upload_documents(dataset_id, folder_path)
        total_uploaded += uploaded
        
        print(f"\n✓ {uploaded} fichiers uploadés pour {folder_name}")
        
        # Attendre un peu avant de lancer le parsing
        time.sleep(2)
        
        # Lancer le parsing
        parse_documents(dataset_id)
        
        # Attendre entre chaque dataset
        print(f"\nAttente de 5 secondes avant le prochain dataset...")
        time.sleep(5)
    
    print(f"\n{'=' * 70}")
    print(f"✓ Upload terminé!")
    print(f"Total de fichiers uploadés: {total_uploaded}")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
