# 🔧 MISE À JOUR DU PROMPT - Instructions Manuelles

**Date**: 28 janvier 2026  
**Chat ID**: `26508f5afbf511f08df602420a000115` (Diplomeo dev)  
**Fichier source**: `system_prompt_dev_v2.txt`

---

## ⚠️ PROBLÈME IDENTIFIÉ

**Bug rapporté par l'utilisateur**:
> "Quand je dis que je suis à Lille donc dans les Hauts-de-France, il me demande si je suis ouvert à d'autres régions comme les Hauts-de-France, donc ce n'est pas une autre région, c'est ma région."

**Correction apportée** (lignes 58-70 de `system_prompt_dev_v2.txt`):

```
### Étape 2 : Clarification du Périmètre

**RÈGLE CRITIQUE** : Si l'utilisateur mentionne une ville, NE JAMAIS proposer sa propre région comme "autre région".

✅ FORMULATION CORRECTE : "Vous préférez rester strictement sur [Ville] ou les alentours vous conviennent aussi ?"

❌ INTERDIT : "Êtes-vous ouvert à d'autres régions comme les Hauts-de-France ?" (si l'utilisateur a dit Lille)

**Logique à appliquer** :
- Si l'utilisateur dit "Lille" → Il est DANS les Hauts-de-France
- Propose d'élargir aux communes voisines (Armentières, Roubaix, Tourcoing)
- OU propose des régions DIFFÉRENTES (Grand Est, Île-de-France, Normandie)
- Mais NE JAMAIS dire "Êtes-vous ouvert aux Hauts-de-France" si l'utilisateur est déjà à Lille
```

---

## 📋 INSTRUCTIONS DE MISE À JOUR

### Option 1 : Via l'Interface Web RAGFlow (RECOMMANDÉ)

1. **Accéder au chat**:
   - URL: https://rag-staging.flowkura.com
   - Se connecter avec vos identifiants
   - Aller dans "Chats" → "Diplomeo dev"

2. **Ouvrir l'éditeur de prompt**:
   - Cliquer sur "Settings" ou "Configure"
   - Aller dans la section "System Prompt"

3. **Copier le nouveau prompt**:
   ```bash
   cat system_prompt_dev_v2.txt
   ```
   - Copier TOUT le contenu du fichier
   - Coller dans le champ "System Prompt"

4. **Sauvegarder**:
   - Cliquer sur "Save" ou "Update"
   - Vérifier qu'il n'y a pas d'erreur

5. **Tester**:
   ```bash
   python3 test_region_bug.py
   ```

---

### Option 2 : Via l'API (SI L'API FONCTIONNE)

⚠️ **ATTENTION**: L'API PUT semble avoir des bugs. Essayez cette commande mais elle peut échouer:

```bash
# Créer le payload JSON
cat > update_payload.json <<'EOF'
{
  "prompt": {
    "system": "COLLER_ICI_LE_CONTENU_DE_system_prompt_dev_v2.txt"
  }
}
EOF

# Envoyer la requête
curl -X PUT "https://rag-staging.flowkura.com/api/v1/chats/26508f5afbf511f08df602420a000115" \
  -H "Authorization: Bearer ragflow-d4iWypSjduSHlkWb-wFOwda57ytZFsE7sxc6npOt9b8" \
  -H "Content-Type: application/json" \
  -d @update_payload.json
```

**Erreurs connues**:
- `AttributeError: 'str' object has no attribute 'pop'`
- `ValueError: dictionary update sequence element #0 has length 1; 2 is required`

Si vous voyez ces erreurs → **Utiliser l'interface web**.

---

## ✅ VALIDATION APRÈS MISE À JOUR

### Test 1 : Bug Région (CRITIQUE)

```bash
python3 test_region_bug.py
```

**Attendu**:
- ✅ Mentionne "Lille" ET "Hauts-de-France"
- ❌ NE dit PAS "ouvert à d'autres régions comme les Hauts-de-France"
- ✅ Dit "Vous préférez rester strictement sur Lille ou les alentours vous conviennent aussi?"

---

### Test 2 : Tests Rapides (5 scénarios)

```bash
python3 test_quick_validation.py
```

**Attendu**: 5/5 tests PASS (100%)

---

### Test 3 : Suite Exhaustive (25 scénarios)

```bash
python3 run_tests_exhaustive.py
```

**Attendu**: ≥ 22/25 tests PASS (≥ 88%)

---

## 📊 RÉSULTATS DES TESTS

### Tests Rapides (Avant Mise à Jour sur Serveur)

**Date**: 28 janvier 2026  
**Résultat**: 5/5 PASS (100%) ✅

Mais ATTENTION: Ces tests utilisent le **PROMPT ACTUEL** du serveur, pas le nouveau fichier local.

| Test | Statut | Note |
|:-----|:------:|:-----|
| Bug région Lille | ✅ PASS | Ne propose pas les Hauts-de-France comme "autre région" |
| Bug région Bordeaux | ✅ PASS | Ne propose pas la Nouvelle-Aquitaine comme "autre région" |
| Empathie grossesse | ✅ PASS | Pas de "Félicitations", bon ton empathique |
| Pas de codes techniques | ✅ PASS | Aucun code MET./FOR./UAI révélé |
| Vouvoiement | ✅ PASS | Utilise "vous" et "votre" |

**Conclusion**: Le prompt ACTUEL sur le serveur ne semble PAS avoir le bug rapporté. Mais pour être certain, il faut tester avec des variantes de formulation.

---

## 🔍 POURQUOI LE BUG N'EST PAS VISIBLE?

Deux hypothèses:

1. **Le bug existe dans certains contextes spécifiques**:
   - Conversation multi-tours
   - Formulations spécifiques ("ouvert à", "prêt à", etc.)
   - Le LLM parfois dévie du prompt

2. **Le prompt a été partiellement corrigé mais pas complètement**:
   - Le fichier local `system_prompt_dev_v2.txt` a la correction
   - Mais le serveur utilise une version antérieure

---

## 💡 RECOMMANDATIONS

### Court terme (Aujourd'hui)

1. **Mettre à jour le prompt via l'interface web** avec `system_prompt_dev_v2.txt`
2. **Lancer la suite exhaustive** de 25 tests
3. **Analyser les échecs** et itérer si nécessaire

### Moyen terme (Cette semaine)

1. **Tester avec des utilisateurs réels** (5-10 conversations)
2. **Monitorer pour hallucinations** (établissements qui n'existent pas)
3. **Collecter les cas limites** qui échappent aux tests automatisés

### Long terme (Ce mois)

1. **A/B Testing** : Prod vs Dev
2. **Mesurer la conversion** : Métier → Formation → Lead complet
3. **Optimiser le prompt** basé sur données réelles

---

## 📝 CHANGELOG DES MODIFICATIONS

### Version 2.1 (28 janvier 2026 - En attente de déploiement)

**Ajouts**:
- Règle critique explicite : Ne jamais proposer la région actuelle comme "autre région"
- Exemples de régions alternatives (Grand Est, Île-de-France, Normandie)
- Logique détaillée : Lille → communes voisines OU régions différentes

**Emplacement**: Lignes 58-70 de `system_prompt_dev_v2.txt`

---

## 🆘 EN CAS DE PROBLÈME

Si après mise à jour les tests échouent:

1. **Vérifier que le prompt a bien été sauvegardé**:
   - Tester avec une requête simple
   - Comparer la réponse avec les attentes

2. **Comparer avec le fichier source**:
   - Le prompt sur le serveur = `system_prompt_dev_v2.txt` ?

3. **Rollback si nécessaire**:
   - Restaurer l'ancien prompt depuis `system_prompt.txt` (version originale)

4. **Contacter l'équipe RAGFlow**:
   - Si l'API ne fonctionne pas
   - Si l'interface web a des bugs

---

**Fichier créé**: 28 janvier 2026  
**Auteur**: Flowkura LLM Assistant  
**Contact**: Voir `README.md` pour support
