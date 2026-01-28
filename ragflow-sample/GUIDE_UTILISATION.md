# 🎓 Guide d'Utilisation : Chat Diplomeo Dev

## 🚀 Accès Rapide

**URL** : https://rag-staging.flowkura.com/  
**Chat ID** : `26508f5afbf511f08df602420a000115`  
**Nom du Chat** : Diplomeo dev  
**API Key** : `ragflow-d4iWypSjduSHlkWb-wFOwda57ytZFsE7sxc6npOt9b8`

---

## 📂 Structure des Fichiers

```
ragflow-sample/
├── 1_metiers/                     # 9 fiches métiers
├── 2_formations/                  # 12 fiches formations
├── 3_actions_formation/           # 120+ actions de formation
├── 4_etablissements/              # 119+ établissements
│
├── chat_configuration.json        # Config PRODUCTION (temp=0.55)
├── chat_dev_info.json            # Config DEV (temp=0.7, top_k=20)
│
├── system_prompt.txt             # Prompt original (production)
├── system_prompt_dev_v2.txt      # Prompt optimisé DEV ✨
├── opener_message.txt            # Message d'accueil
│
├── run_tests.py                  # Script de tests automatisés
├── TEST_REPORT_20260128_FINAL.md # Rapport de test complet
├── MISSION_ACCOMPLISHED.md       # Résumé de la mission
│
└── CONFIGURATION_COMPARISON.md   # Comparaison prod/dev
```

---

## 🧪 Tester le Chat via API

### Test Manuel Simple

```bash
curl -X POST "https://rag-staging.flowkura.com/api/v1/chats_openai/26508f5afbf511f08df602420a000115/chat/completions" \
  -H "Authorization: Bearer ragflow-d4iWypSjduSHlkWb-wFOwda57ytZFsE7sxc6npOt9b8" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen",
    "messages": [
      {"role": "user", "content": "Je cherche une formation de comptabilité à Lille."}
    ],
    "stream": false
  }' | jq '.choices[0].message.content'
```

### Tests Automatisés

```bash
cd ragflow-sample
python3 run_tests.py
```

**Output** :
- `TEST_REPORT_YYYYMMDD_HHMMSS.md` : Rapport détaillé
- `TEST_RESULTS_YYYYMMDD_HHMMSS.json` : Résultats bruts JSON

---

## 🎯 Scénarios de Test Préparés

### 1️⃣ Entonnoir Régional
**Test** : "Je cherche une formation de comptabilité à Lille."  
**Attendu** :
- ✅ Mention de "Hauts-de-France"
- ✅ Proposition d'élargir ("strictement sur Lille ou alentours")
- ✅ Pas de "Super, Lille !"

### 2️⃣ Empathie
**Test** : "Je suis enceinte et je dois me reconvertir sur Bordeaux."  
**Attendu** :
- ✅ Empathie EN PREMIER ("C'est un moment important...")
- ✅ Pas de "Félicitations !"
- ✅ Mention de "Nouvelle-Aquitaine"

### 3️⃣ Chaîne Complète
**Test** : "Je veux être infirmier à Lille."  
**Attendu** :
- ✅ Mention du DEI (3 ans, Bac+3)
- ✅ Hauts-de-France mentionné
- ✅ Établissements présentés sans codes UAI
- ✅ Pas de "Voici les écoles" → "J'ai sélectionné ces établissements"

---

## 🔧 Modifier le Prompt Système

### Via l'API

```bash
curl -X PUT "https://rag-staging.flowkura.com/api/v1/chats/26508f5afbf511f08df602420a000115" \
  -H "Authorization: Bearer ragflow-d4iWypSjduSHlkWb-wFOwda57ytZFsE7sxc6npOt9b8" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": {
      "prompt": "VOTRE_NOUVEAU_PROMPT_ICI"
    }
  }'
```

### Workflow Recommandé

1. **Éditer** : Modifier `system_prompt_dev_v2.txt`
2. **Tester** : Lancer `python3 run_tests.py`
3. **Valider** : Vérifier le rapport de test
4. **Déployer** : Update via API
5. **Commit** : `git add` + `git commit`

---

## 📊 Métriques à Surveiller

### Qualité des Réponses
- ✅ **Entonnoir géographique** : Toujours Région → Ville ?
- ✅ **Empathie** : Gestion des situations de vie appropriée ?
- ✅ **Sécurité** : Aucun code technique révélé ?
- ✅ **Ton** : Vouvoiement constant ?

### Performance
- ⏱️ **Temps de réponse** : < 10 secondes idéalement
- 📏 **Longueur des réponses** : 200-400 mots optimal
- 🎯 **Précision** : Établissements mentionnés existent dans le dataset ?

### Conversion Lead
- 📍 **Localisation obtenue** : % des conversations
- 📞 **Contact fourni** : % avec numéro/email d'établissement
- ✅ **Lead qualifié** : Métier + Formation + Localisation + Contact

---

## 🚨 Checklist de Sécurité

Avant chaque modification du prompt, vérifier :

- [ ] ❌ Aucune mention de "Qwen", "GPT", "modèle", "IA"
- [ ] ❌ Aucun code technique (FOR.xxx, MET.xxx, UAI, ROME)
- [ ] ❌ Aucune URL ou lien du dataset
- [ ] ❌ Pas de "dataset", "documents", "base de données"
- [ ] ✅ Vouvoiement systématique
- [ ] ✅ Empathie face aux situations de vie
- [ ] ✅ Entonnoir géographique appliqué

---

## 🎓 Mapping Géographique

### Villes → Régions Implémentées

| Ville | Région | Académie |
|:------|:-------|:---------|
| Lille | Hauts-de-France | Lille |
| Bordeaux | Nouvelle-Aquitaine | Bordeaux |
| Lyon | Auvergne-Rhône-Alpes | Lyon |
| Nancy | Grand Est | Nancy-Metz |
| Rennes | Bretagne | Rennes |
| Armentières | Hauts-de-France | Lille |

### Ajouter une Nouvelle Ville

1. Identifier la région administrative
2. Ajouter dans `system_prompt_dev_v2.txt` :
   ```
   - NouvelleVille → Région
   ```
3. Tester avec un scénario
4. Commit

---

## 🔍 Debugging

### Le bot ne mentionne pas la région

**Problème** : Réponse sans "Hauts-de-France", "Nouvelle-Aquitaine", etc.

**Solution** :
1. Vérifier que la ville est dans le mapping du prompt
2. Tester avec un cas simple : "Je cherche une formation à [Ville]."
3. Vérifier les logs de l'API pour erreurs

### Le bot révèle des codes techniques

**Problème** : Codes FOR.xxx, MET.xxx visibles dans la réponse

**Solution** :
1. Vérifier la section "Sécurité et Confidentialité" du prompt
2. Renforcer les interdictions : "Ne JAMAIS mentionner..."
3. Tester immédiatement après modification

### Hallucinations d'établissements

**Problème** : Le bot invente des écoles qui n'existent pas

**Solution** :
1. Vérifier que l'établissement existe dans `4_etablissements/`
2. Si manquant, ajouter au dataset
3. Ajouter un disclaimer : "Je vous propose ces pistes, vérifiez la disponibilité"

---

## 📞 Support et Contact

### Pour Questions Techniques
- **GitHub Issues** : [Lien vers votre repo]
- **Documentation** : Ce fichier + `MISSION_ACCOMPLISHED.md`

### Pour Modifications Urgentes
1. Éditer le prompt via l'interface RAGFlow
2. Tester manuellement avec 2-3 requêtes
3. Documenter la modification dans un commit

---

## 🎯 Prochaines Étapes

### Court Terme (Cette Semaine)
- [ ] Tester avec 10 utilisateurs réels
- [ ] Collecter les feedbacks
- [ ] Ajuster le prompt si nécessaire
- [ ] Mesurer le taux de conversion lead

### Moyen Terme (Mois Prochain)
- [ ] Comparer performances prod vs dev
- [ ] Décider si passage en production
- [ ] Enrichir le dataset (plus d'établissements)
- [ ] Implémenter des métriques de satisfaction

### Long Terme (Trimestre)
- [ ] A/B testing prod vs dev
- [ ] Optimisation continue du prompt
- [ ] Intégration de nouveaux datasets
- [ ] Amélioration de l'empathie via feedback utilisateur

---

## ✅ Validation Finale

Avant de déployer en production, vérifier :

1. **Tests passent** : `python3 run_tests.py` → 3/3 PASS
2. **Sécurité OK** : Aucun code technique visible
3. **Empathie OK** : Situations de vie gérées correctement
4. **Géo OK** : Entonnoir Région → Ville systématique
5. **Feedbacks OK** : Utilisateurs satisfaits (>80%)

---

**Bon test !** 🚀

*Si vous avez des questions, consultez `TEST_REPORT_20260128_FINAL.md` ou `MISSION_ACCOMPLISHED.md`*
