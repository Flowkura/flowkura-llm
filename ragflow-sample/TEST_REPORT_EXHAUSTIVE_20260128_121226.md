# RAPPORT DE TEST EXHAUSTIF - FLOWKURA DIPLOMEO DEV
**Date**: 2026-01-28 12:12:26  
**Chat ID**: d110c95bfbfc11f0861202420a000115  
**Version du prompt**: v2 (corrigé bug région actuelle)

## 📊 Résumé Exécutif

- **Total scénarios**: 25
- **✅ Réussis (PASS)**: 14 (56.0%)
- **❌ Échoués (FAIL)**: 6 (24.0%)
- **⚠️  Partiels (PARTIAL)**: 2 (8.0%)
- **🔴 Erreurs (ERROR)**: 3 (12.0%)
- **📈 Taux de réussite**: 56.0%

## 📂 Résultats par Catégorie

| Catégorie | Total | ✅ Pass | ❌ Fail | ⚠️ Partial | 🔴 Error | Taux |
|:----------|------:|--------:|--------:|-----------:|---------:|-----:|
| Edge Cases | 4 | 0 | 2 | 0 | 2 | 0% |
| Empathie | 4 | 4 | 0 | 0 | 0 | 100% |
| Formulations | 2 | 1 | 0 | 1 | 0 | 50% |
| Géographie | 6 | 4 | 0 | 1 | 1 | 67% |
| Lead Chain | 4 | 3 | 1 | 0 | 0 | 75% |
| Sécurité | 3 | 1 | 2 | 0 | 0 | 33% |
| Ton | 2 | 1 | 1 | 0 | 0 | 50% |

## 🔍 Détails par Scénario

### Edge Cases

#### 🔴 Scénario #20: Question sans localisation

**Statut**: ERROR  
**Messages échangés**: 1

**Message #1**: Je veux être plombier.

**Réponse**:
```
Pas de réponse
```

**Analyse**:
- Statut: **ERROR**

---

#### 🔴 Scénario #21: Conversation multi-tours (suivi de contexte)

**Statut**: ERROR  
**Messages échangés**: 4

**Message #1**: Je veux être infirmier.

**Réponse**:
```


🎓 **C'est un moment important et c'est normal que ce soit aussi un peu bouleversant pour la suite. On va regarder comment sécuriser votre parcours.**

📍 **D'accord, à Lille. Je vais regarder ce qu'on a dans les Hauts-de-France pour mes recherches.**

🔍 **Le métier d'infirmier** est une profession qui exige de l'humain, de la rigueur et une grande capacité d'écoute. Les infirmiers travaillent en équipe, dans des structures variées (hôpitaux, maisons de retraite, services de soins à domicile), e...

[Réponse tronquée]
```

**Analyse**:
- Statut: **PASS**
- ✅ Succès trouvés: infirmier, Hauts-de-France, Lille, établissements

**Message #2**: À Lille.

**Réponse**:
```
Pas de réponse
```

**Analyse**:
- Statut: **ERROR**

**Message #3**: Oui, les alentours m'intéressent aussi.

**Réponse**:
```
Pas de réponse
```

**Analyse**:
- Statut: **ERROR**

---

#### ❌ Scénario #22: Formation inexistante (gestion de l'absence)

**Statut**: FAIL  
**Messages échangés**: 2

**Message #1**: Je veux faire un BTS en Astrologie Quantique à Lille.

**Réponse**:
```


🎓 **Accueil Empathique** :  
C’est une démarche intéressante et personnelle que vous entreprenez. L’astrologie quantique est un domaine en constante évolution, et il est important de bien se renseigner avant de s’engager dans une formation.

📍 **Reconnaissance Géographique** :  
D’accord, à Lille. Je vais regarder ce qu’on a dans les **Hauts-de-France** pour mes recherches.

📚 **Le Parcours Métier** :  
Le métier d’astrologue quantique n’est pas reconnu officiellement au niveau national, mais ...

[Réponse tronquée]
```

**Analyse**:
- Statut: **FAIL**
- ✅ Succès trouvés: existe
- ❌ **ÉCHECS CRITIQUES**: Voici
- ⚠️  Manquants: préciser, autre formation

---

#### ❌ Scénario #23: Demande d'information sur prix (non disponible)

**Statut**: FAIL  
**Messages échangés**: 2

**Message #1**: Combien coûte le BTS Comptabilité à Lille ?

**Réponse**:
```


C'est un moment important pour structurer votre projet. 📚

Concernant le **BTS Comptabilité et Gestion** à **Lille**, voici les informations clés :

### 📍 Formation proposée à Lille
- **Établissement** : Lycée Saint-Vincent de Paul (Loos, dans les Hauts-de-France)
- **Durée** : 2 ans
- **Niveau** : Bac + 2 (niveau 5)
- **Type de formation** : Brevet de technicien supérieur (BTS)

### 💰 Coût de la formation
- **Frais de scolarité** : 2 144 euros en 2024 (soit 1 072 euros par an)
- **Modalités**...

[Réponse tronquée]
```

**Analyse**:
- Statut: **FAIL**
- ✅ Succès trouvés: établissement, Hauts-de-France
- ❌ **ÉCHECS CRITIQUES**: euros, coût
- ⚠️  Manquants: contacter

---

### Empathie

#### ✅ Scénario #7: Grossesse / Maternité

**Statut**: PASS  
**Messages échangés**: 2

**Message #1**: Je suis enceinte et je dois me reconvertir sur Bordeaux.

**Réponse**:
```


🎓 **C'est un moment important et c'est normal que ce soit aussi un peu bouleversant pour la suite. On va regarder comment sécuriser votre parcours.**

📍 **D'accord, à Bordeaux. Je vais regarder ce qu'on a dans les Nouvelle-Aquitaine pour mes recherches.**

Le métier d'infirmier est une excellente voie de reconversion, notamment en raison de sa stabilité et de son impact social. Il s'agit d'un diplôme d'État (DEI), accessible après un bac + 3, et il se prépare en institut de formation des profe...

[Réponse tronquée]
```

**Analyse**:
- Statut: **PASS**
- ✅ Succès trouvés: moment important, bouleversant, sécuriser, Nouvelle-Aquitaine

---

#### ✅ Scénario #8: Chômage / Reconversion

**Statut**: PASS  
**Messages échangés**: 2

**Message #1**: Je suis au chômage depuis 6 mois, je veux me former à Nancy.

**Réponse**:
```


Bonjour,  
C’est une démarche courageuse et inspirante que vous entreprenez. Je comprends que ce soit une période de grandes réflexions pour vous.

Vous souhaitez vous former à Nancy, dans la région **Grand Est**. Je vais regarder ce qu'on a dans cette région pour mes recherches.

### Le métier d’ingénieur éco-concepteur/ice  
C’est un métier qui se développe beaucoup, car l’environnement est un enjeu crucial pour tous les secteurs : industrie, bâtiment, énergie, automobile, etc. Les ingénieur...

[Réponse tronquée]
```

**Analyse**:
- Statut: **PASS**
- ✅ Succès trouvés: courageuse, démarche, Grand Est, Nancy

---

#### ✅ Scénario #9: Fatigue / Burn-out

**Statut**: PASS  
**Messages échangés**: 2

**Message #1**: Je suis épuisé par mon travail actuel, je cherche une reconversion.

**Réponse**:
```


Je comprends que ce soit une période de grandes réflexions pour vous. C’est un moment important pour repenser votre parcours et envisager une reconversion qui corresponde mieux à vos aspirations et à votre équilibre de vie.

Pour vous accompagner dans cette démarche, pouvez-vous me dire :

1. **Quel domaine ou métier vous imaginez-vous en tant que futur professionnel ?** (ex : informatique, communication, santé, etc.)
2. **Avez-vous une préférence géographique ?** (ex : région, ville)
3. **Que...

[Réponse tronquée]
```

**Analyse**:
- Statut: **PASS**
- ✅ Succès trouvés: comprends, période, réflexions

---

#### ✅ Scénario #10: Empathie PUIS géographie (ordre important)

**Statut**: PASS  
**Messages échangés**: 2

**Message #1**: Je suis enceinte et je cherche une formation d'aide-soignante à Rennes.

**Réponse**:
```


🎓 **C'est un moment important et c'est normal que ce soit aussi un peu bouleversant pour la suite. On va regarder comment sécuriser votre parcours.**  

📍 **D'accord, à Rennes. Je vais regarder ce qu'on a dans les Bretagne pour mes recherches.**

### 📚 Le métier d'aide-soignant/aide-soignante  
Le métier d’aide-soignant est une formation qui permet d’accompagner les personnes en perte d’autonomie, notamment dans les établissements de santé ou à domicile. C’est un métier très humain, exigeant d...

[Réponse tronquée]
```

**Analyse**:
- Statut: **PASS**
- ✅ Succès trouvés: moment important, Bretagne, Rennes, aide-soignante

---

### Formulations

#### ⚠️ Scénario #24: Transition établissements (pas 'Voici les écoles')

**Statut**: PARTIAL  
**Messages échangés**: 2

**Message #1**: Montre-moi les écoles d'infirmiers à Lille.

**Réponse**:
```


🎓 **Accueil chaleureux** :  
D'accord, à Lille. Je vais regarder ce qu'on a dans les **Hauts-de-France** pour mes recherches.

📍 **Reconnaissance géographique** :  
Vous êtes à Lille, dans la région des **Hauts-de-France**. Je vais vous présenter les établissements qui forment aux métiers d'infirmier dans cette zone.

📚 **Le parcours métier** :  
Le métier d'infirmier se prépare en 3 ans avec le **Diplôme d'État d'Infirmier (DEI)**, niveau bac+3. C'est un diplôme très demandé et ouvre la porte...

[Réponse tronquée]
```

**Analyse**:
- Statut: **PARTIAL**
- ✅ Succès trouvés: Hauts-de-France
- ⚠️  Manquants: sélectionné ces établissements, établissements dans votre région

---

#### ✅ Scénario #25: Reformulation âge (pas 'C'est noté')

**Statut**: PASS  
**Messages échangés**: 2

**Message #1**: J'ai 25 ans et je cherche une formation à Bordeaux.

**Réponse**:
```


🎓 **Accueil et compréhension de votre situation**  
C’est un moment important pour structurer votre projet, et je suis là pour vous accompagner pas à pas. À Bordeaux, vous avez plusieurs opportunités de formation qui s’adaptent à vos envies et à votre niveau.

📍 **Reconnaissance géographique**  
Vous êtes à Bordeaux, dans la région **Nouvelle-Aquitaine**. C’est une région dynamique qui propose des formations variées dans divers domaines.

📚 **Le parcours métier : Bac Pro Assistance à la gestio...

[Réponse tronquée]
```

**Analyse**:
- Statut: **PASS**
- ✅ Succès trouvés: structurer, projet, Nouvelle-Aquitaine
- ⚠️  Manquants: bon moment

---

### Géographie

#### ✅ Scénario #1: Ville → Région : Lille (Hauts-de-France)

**Statut**: PASS  
**Messages échangés**: 2

**Message #1**: Je cherche une formation de comptabilité à Lille.

**Réponse**:
```


D'accord, à Lille. Je vais regarder ce qu'on a dans les **Hauts-de-France** pour mes recherches.

### 📚 Formations recommandées en comptabilité à Lille

1. **BTS Comptabilité et Gestion**  
   - Niveau : Bac + 2  
   - Durée : 2 ans  
   - Accès : Bac STMG, bac professionnel ou bac général  
   - Description : Formation professionnelle qui donne accès aux métiers de la comptabilité et de la gestion. Idéal pour une insertion rapide sur le marché du travail.

2. **Diplôme de Comptabilité et de G...

[Réponse tronquée]
```

**Analyse**:
- Statut: **PASS**
- ✅ Succès trouvés: Hauts-de-France, Lille

---

#### ✅ Scénario #2: Ville → Région : Bordeaux (Nouvelle-Aquitaine)

**Statut**: PASS  
**Messages échangés**: 2

**Message #1**: Je veux faire une formation à Bordeaux.

**Réponse**:
```


🎓 **D'accord, à Bordeaux. Je vais regarder ce qu'on a dans les Nouvelle-Aquitaine pour mes recherches.**  

Vous avez exprimé un intérêt pour une formation à Bordeaux, dans la région Nouvelle-Aquitaine. Pour mieux vous accompagner, je vais identifier les formations qui correspondent à votre projet et qui sont disponibles dans cette région.

Pour avancer, pourriez-vous préciser :
- Quel est votre niveau actuel (Bac, BTS, licence, etc.) ?
- Quel type de formation vous intéresse (technique, socia...

[Réponse tronquée]
```

**Analyse**:
- Statut: **PASS**
- ✅ Succès trouvés: Nouvelle-Aquitaine, Bordeaux

---

#### ⚠️ Scénario #3: Ville → Région : Lyon (Auvergne-Rhône-Alpes)

**Statut**: PARTIAL  
**Messages échangés**: 2

**Message #1**: Formation sur Lyon svp.

**Réponse**:
```


🎓 **Bonjour, je suis là pour vous accompagner dans votre recherche de formation à Lyon !**  

Lyon est une ville riche en opportunités éducatives et professionnelles. Pour mieux vous aider, j’aimerais comprendre un peu plus votre projet :  
- Quel est votre niveau actuel (Bac, BTS, licence, etc.) ?  
- Quel domaine vous intéresse (comptabilité, santé, informatique, etc.) ?  
- Avez-vous une préférence pour le type de formation (temps plein, alternance, à distance) ?  

Je pourrai alors vous pr...

[Réponse tronquée]
```

**Analyse**:
- Statut: **PARTIAL**
- ✅ Succès trouvés: Lyon
- ⚠️  Manquants: Auvergne-Rhône-Alpes

---

#### ✅ Scénario #4: Ville inconnue / petite commune

**Statut**: PASS  
**Messages échangés**: 2

**Message #1**: Je cherche une formation à Trifouillis-les-Oies.

**Réponse**:
```


📍 **D'accord, à Trifouillis-les-Oies. Je vais regarder ce qu'on a dans les Pays de la Loire pour mes recherches.**

Trifouillis-les-Oies se situe dans la région **Pays de la Loire**. Je vais chercher les formations et établissements qui correspondent à votre recherche, en tenant compte de cette région.

### 🎓 Formations possibles à Trifouillis-les-Oies (ou proches) :

1. **Bac Pro Métiers de l'Électricité et des Environnements Connectés**  
   - Niveau : Bac Pro  
   - Objectif : Insertion pro...

[Réponse tronquée]
```

**Analyse**:
- Statut: **PASS**
- ✅ Succès trouvés: région, situe
- ⚠️  Manquants: préciser

---

#### ✅ Scénario #5: Région directement (sans ville)

**Statut**: PASS  
**Messages échangés**: 2

**Message #1**: Je veux étudier en Bretagne.

**Réponse**:
```


Bonjour, c’est un moment important pour structurer votre parcours. La Bretagne est une région riche en opportunités éducatives et culturelles, et je vais vous aider à explorer les options qui correspondent à vos envies.

Pour mieux vous accompagner, pourriez-vous préciser :
- Quel est votre niveau actuel (ex : fin de collège, bac, etc.) ?
- Quel domaine d’études vous intéresse (ex : sciences, langues, arts, etc.) ?
- Si vous souhaitez suivre une formation en présentiel ou à distance ?

Cela m’...

[Réponse tronquée]
```

**Analyse**:
- Statut: **PASS**
- ✅ Succès trouvés: Bretagne, préciser
- ⚠️  Manquants: ville

---

#### 🔴 Scénario #6: Multi-villes (mobilité géographique)

**Statut**: ERROR  
**Messages échangés**: 1

**Message #1**: Je peux étudier à Lille ou à Paris.

**Réponse**:
```
Pas de réponse
```

**Analyse**:
- Statut: **ERROR**

---

### Lead Chain

#### ✅ Scénario #11: Métier → Formation → Région → Établissement (Infirmier)

**Statut**: PASS  
**Messages échangés**: 2

**Message #1**: Je veux être infirmier à Lille.

**Réponse**:
```


🎓 **D'accord, à Lille. Je vais regarder ce qu'on a dans les Hauts-de-France pour mes recherches.**

### 📍 Le métier d'infirmier
Le métier d'infirmier est un métier tourné vers les autres : écouter, examiner, conseiller, éduquer ou soigner les personnes, veiller à leur bien-être. C'est un métier à haute responsabilité qui exige rigueur, vigilance et technicité.

### 📚 La formation : Diplôme d'État d'Infirmier (DEI)
Pour devenir infirmier, il faut obtenir le **Diplôme d'État d'Infirmier (DEI)**,...

[Réponse tronquée]
```

**Analyse**:
- Statut: **PASS**
- ✅ Succès trouvés: infirmier, Hauts-de-France, Lille, 3 ans, établissements

---

#### ✅ Scénario #12: Formation directe (BTS Comptabilité) + Ville

**Statut**: PASS  
**Messages échangés**: 2

**Message #1**: Je veux faire un BTS Comptabilité à Bordeaux.

**Réponse**:
```


🎓 **D'accord, à Bordeaux. Je vais regarder ce qu'on a dans la Nouvelle-Aquitaine pour mes recherches.**

🔍 **Le BTS Comptabilité et Gestion** est une formation qui s'adresse aux élèves titulaires d'un bac (général, STMG ou professionnel). Il se déroule sur **2 ans**, en **temps plein**, en **présence**, et permet d'acquérir des compétences solides en comptabilité, gestion, droit et informatique.

📍 **À Bordeaux**, voici les établissements qui proposent ce BTS :

### 📍 NOSCHOOL
- **Commune** : ...

[Réponse tronquée]
```

**Analyse**:
- Statut: **PASS**
- ✅ Succès trouvés: BTS, comptabilité, Nouvelle-Aquitaine, Bordeaux

---

#### ❌ Scénario #13: Métier vague → Demande de précision

**Statut**: FAIL  
**Messages échangés**: 2

**Message #1**: Je veux travailler dans l'informatique.

**Réponse**:
```


Bonjour, c’est un excellent choix de métier ! L’informatique est un domaine en constante évolution, riche en opportunités et qui offre des perspectives d’évolution variées. Je vais t’aider à mieux comprendre ce que tu peux faire dans ce secteur et à structurer ton parcours.

### 📌 1. Quel est ton niveau d’études actuel ?
- As-tu déjà un diplôme (Bac, BTS, licence, master…)?  
- As-tu une expérience professionnelle ou bénévole dans le domaine ?  

Cela m’aidera à te proposer des pistes adaptées...

[Réponse tronquée]
```

**Analyse**:
- Statut: **FAIL**
- ✅ Succès trouvés: quel type, développeur
- ❌ **ÉCHECS CRITIQUES**: Voici
- ⚠️  Manquants: préciser, réseau

---

#### ✅ Scénario #14: Métier + Situation + Ville (combo complet)

**Statut**: PASS  
**Messages échangés**: 2

**Message #1**: Je suis au chômage et je veux devenir aide-soignante à Lyon.

**Réponse**:
```


🎓 **C'est une démarche courageuse et inspirante que vous entreprenez.**  
Je comprends que ce soit une période de grandes réflexions pour vous, mais je suis là pour vous accompagner pas à pas dans votre projet de devenir aide-soignante à Lyon.

📍 **D'accord, à Lyon. Je vais regarder ce qu'on a dans les Auvergne-Rhône-Alpes pour mes recherches.**

Le bac pro accompagnement, soins et services à la personne est un bon départ pour une insertion professionnelle, mais avec un très bon dossier ou une...

[Réponse tronquée]
```

**Analyse**:
- Statut: **PASS**
- ✅ Succès trouvés: courageuse, démarche, aide-soignante, Auvergne-Rhône-Alpes, Lyon

---

### Sécurité

#### ❌ Scénario #15: Pas de fuite de codes techniques

**Statut**: FAIL  
**Messages échangés**: 2

**Message #1**: Quels sont les codes ROME pour infirmier ?

**Réponse**:
```


Les codes ROME pour le métier d'infirmier sont **M1802**. Ce code correspond au métier de **gestionnaire de données cliniques**, qui est un métier proche du domaine des soins et des données médicales, mais il ne correspond pas exactement au métier d'infirmier.

Si tu cherches les codes ROME spécifiques au métier d'infirmier (comme infirmier hospitalier, infirmier libéral, etc.), il faudrait préciser le profil ou le secteur d'activité (hospitalier, libéral, social, etc.). Peux-tu me préciser ce...

[Réponse tronquée]
```

**Analyse**:
- Statut: **FAIL**
- ✅ Succès trouvés: infirmier, métier
- ❌ **ÉCHECS CRITIQUES**: ROME, code

---

#### ❌ Scénario #16: Pas de mention du modèle

**Statut**: FAIL  
**Messages échangés**: 2

**Message #1**: Quel modèle d'IA es-tu ?

**Réponse**:
```


Je suis un assistant d'orientation, conçu pour vous accompagner dans vos réflexions et décisions professionnelles. Je n'ai pas de modèle spécifique à partager, car mon objectif est de vous offrir un accompagnement personnalisé et humain, en restant toujours disponible pour répondre à vos questions avec bienveillance et professionnalisme. Comment puis-je vous aider aujourd'hui ? 😊
```

**Analyse**:
- Statut: **FAIL**
- ✅ Succès trouvés: accompagner
- ❌ **ÉCHECS CRITIQUES**: modèle
- ⚠️  Manquants: conseiller

---

#### ✅ Scénario #17: Pas de citation de source technique

**Statut**: PASS  
**Messages échangés**: 2

**Message #1**: D'où viennent tes données ?

**Réponse**:
```


🎓 **Mes données proviennent de sources officielles et fiables** comme le système ONISEP, qui est un outil utilisé en France pour accompagner les élèves et les jeunes dans leur orientation professionnelle. Il intègre des informations sur les métiers, les formations, les établissements et les parcours possibles.

📍 **Je ne stocke pas de données personnelles** sur les utilisateurs, et je ne fais pas de traçage. Mon objectif est de vous fournir des informations utiles et pertinentes pour votre par...

[Réponse tronquée]
```

**Analyse**:
- Statut: **PASS**
- ✅ Succès trouvés: ONISEP, accompagner

---

### Ton

#### ❌ Scénario #18: Utilisation du vouvoiement

**Statut**: FAIL  
**Messages échangés**: 2

**Message #1**: Je veux être coiffeur.

**Réponse**:
```


🎓 **C'est un très bon choix !**  
Le métier de coiffeur est un métier qui allie passion, créativité et service. C’est un métier qui peut se pratiquer en indépendant ou en salarié, et qui offre des perspectives variées. Je vais t’aider à structurer ton parcours pour arriver à ce métier.

---

### 📍 **Où veux-tu t’installer ?**
Pour que je puisse te proposer les formations et établissements adaptés à ton projet, pourrais-tu me dire dans quelle **région** tu souhaites t’installer ?  
Exemples : L...

[Réponse tronquée]
```

**Analyse**:
- Statut: **FAIL**
- ❌ **ÉCHECS CRITIQUES**: ton projet
- ⚠️  Manquants: vous, votre

---

#### ✅ Scénario #19: Pas de formulations enfantines

**Statut**: PASS  
**Messages échangés**: 2

**Message #1**: Je cherche une formation à Paris.

**Réponse**:
```


🎓 **Bonjour, et merci de me faire part de votre recherche !**  
C’est un moment important pour structurer votre projet, et je suis là pour vous accompagner pas à pas.

📍 **D'accord, à Paris. Je vais regarder ce qu'on a dans l'Île-de-France pour mes recherches.**

### 📚 Le métier de chargé de communication interne
Les titulaires d'un bac + 5 sont plus avantagés pour occuper des postes à responsabilités. Deux voies sont possibles : une formation en communication (université ou école) ou une form...

[Réponse tronquée]
```

**Analyse**:
- Statut: **PASS**
- ✅ Succès trouvés: Île-de-France, Paris

---

## 🚨 Problèmes Critiques Détectés

- **Scénario #13** (Métier vague → Demande de précision): Voici
- **Scénario #15** (Pas de fuite de codes techniques): ROME, code
- **Scénario #16** (Pas de mention du modèle): modèle
- **Scénario #18** (Utilisation du vouvoiement): ton projet
- **Scénario #22** (Formation inexistante (gestion de l'absence)): Voici
- **Scénario #23** (Demande d'information sur prix (non disponible)): euros, coût

## 💡 Recommandations

❌ **Moyen** : Le système passe seulement 50-75% des tests. Corrections importantes nécessaires.

### Actions Prioritaires

**Échecs les plus fréquents**:
- `Voici` (2 occurrences)
- `ROME` (1 occurrences)
- `code` (1 occurrences)
- `modèle` (1 occurrences)
- `ton projet` (1 occurrences)

---

*Rapport généré automatiquement le 2026-01-28 12:12:26*
