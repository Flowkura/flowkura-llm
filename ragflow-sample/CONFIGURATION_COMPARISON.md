# Comparaison des Configurations Chat

## Chat Production : "Diplomeo"
**ID** : `1098c60ff69f11f0965902420a000115`

### Paramètres LLM
- **Model** : Qwen/Qwen3___VLLM@VLLM
- **Temperature** : 0.55
- **Top P** : 0.8
- **Presence Penalty** : 0.5
- **Frequency Penalty** : 0.5

### Notes
Configuration originale pour la production.

---

## Chat Développement : "Diplomeo dev"
**ID** : `26508f5afbf511f08df602420a000115`

### Paramètres LLM (optimisés pour /no_think)
- **Model** : Qwen/Qwen3___VLLM@VLLM
- **Temperature** : 0.7 ⬆️ (+0.15)
- **Top P** : 0.8 ✓ (identique)
- **Top K** : 20 ✨ (nouveau)
- **Presence Penalty** : 0.5 ✓ (identique)
- **Frequency Penalty** : 0.5 ✓ (identique)

### Notes
Configuration conforme aux recommandations pour le mode `/no_think` :
- Temperature=0.7
- TopP=0.8
- TopK=20
- MinP=0 (non supporté par l'API RAGFlow)

### Différences Clés
1. **Temperature augmentée à 0.7** : Plus de créativité et variabilité dans les réponses
2. **TopK=20** : Limite le sampling aux 20 tokens les plus probables
3. Tous les autres paramètres restent identiques (datasets, prompts, rerank model, etc.)

---

## Paramètres Communs

### Datasets (4)
1. **Métiers** (`dc762171fb2811f0a03402420a000115`) - 9 docs, 46 chunks
2. **Formations** (`e1c6982ffb2811f0a05d02420a000115`) - 12 docs, 31 chunks
3. **Actions de Formation** (`e8ad1a3afb2811f09a1f02420a000115`) - 120 docs, 181 chunks
4. **Établissements** (`29b4d83bfb2911f0bbfa02420a000115`) - 119 docs, 122 chunks

### Prompt Configuration
- **Top N** : 8
- **Similarity Threshold** : 0.2
- **Keywords Similarity Weight** : 0.7
- **Rerank Model** : BAAI/bge-reranker-v2-m3
- **Show Quote** : false
- **Refine Multiturn** : false

### System Prompt
Identique pour les deux chats - Conseiller d'orientation ONISEP avec empathie et support pour transitions de vie.
