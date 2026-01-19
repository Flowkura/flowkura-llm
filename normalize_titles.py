#!/usr/bin/env python3
"""
Script de normalisation des titres de métiers pour améliorer la recherche RAG.
Résout le problème de l'écriture inclusive (développeur/euse → développeur, développeuse).

Version simplifiée et robuste.
"""

import re
import os
from pathlib import Path


# Dictionnaire des cas spéciaux en dur (métiers composés complexes)
HARDCODED_EXPANSIONS = {
    # Métiers avec tirets (mot1/suffix1-mot2/suffix2)
    "ajusteur/euse-monteur/euse": ["ajusteur-monteur", "ajusteuse-monteuse"],
    "chauffeur/euse-livreur/euse": ["chauffeur-livreur", "chauffeuse-livreuse"],
    "monteur/euse-câbleur/euse": ["monteur-câbleur", "monteuse-câbleuse"],
    "monteur/euse-vendeur/euse": ["monteur-vendeur", "monteuse-vendeuse"],
    "monteur/euse-vendeur/euse  en optique-lunetterie": [
        "monteur-vendeur en optique-lunetterie",
        "monteuse-vendeuse en optique-lunetterie",
    ],
    "mouleur/euse-noyauteur/euse": ["mouleur-noyauteur", "mouleuse-noyauteuse"],
    "relieur/euse-doreur/euse": ["relieur-doreur", "relieuse-doreuse"],
    "bijoutier/ère-joaillier/ère": ["bijoutier-joaillier", "bijoutière-joaillière"],
    "serrurier/ère-métallier/ère": ["serrurier-métallier", "serrurière-métallière"],
    "glacier/ère-sorbetier/ère": ["glacier-sorbetier", "glacière-sorbetière"],
    "vendeur/euse-magasinier/ère": ["vendeur-magasinier", "vendeuse-magasinière"],
    "vendeur/euse-magasinier/ère en fournitures automobiles": [
        "vendeur-magasinier en fournitures automobiles",
        "vendeuse-magasinière en fournitures automobiles",
    ],
    "chirurgien/ne-dentiste": ["chirurgien-dentiste", "chirurgienne-dentiste"],
    "esthéticien/ne-cosméticien/ne": [
        "esthéticien-cosméticien",
        "esthéticienne-cosméticienne",
    ],
    "concepteur/trice-rédacteur/trice": [
        "concepteur-rédacteur",
        "conceptrice-rédactrice",
    ],
    "dessinateur/trice-projeteur/euse": [
        "dessinateur-projeteur",
        "dessinatrice-projeteuse",
    ],
    "moniteur/trice-éducateur/trice": ["moniteur-éducateur", "monitrice-éducatrice"],
    "charcutier/ère-traiteur/euse": ["charcutier-traiteur", "charcutière-traiteuse"],
    "chocolatier/ère-confiseur/euse": [
        "chocolatier-confiseur",
        "chocolatière-confiseuse",
    ],
    "mécanicien/ne-outilleur/euse": ["mécanicien-outilleur", "mécanicienne-outilleuse"],
    "opticien/ne-lunetier/ère": ["opticien-lunetier", "opticienne-lunetière"],
    "patronnier/ère-gradeur/euse": ["patronnier-gradeur", "patronnière-gradeuse"],
    # Cas spéciaux avec accents/particularités
    "maréchal/e-ferrant/e": ["maréchal-ferrant", "maréchale-ferrante"],
    "solier/ère-moquettiste": ["solier-moquettiste", "solière-moquettiste"],
    "écrivain/ne public": ["écrivain public", "écrivaine publique"],
    # Cas avec auteur/compositeur
    "auteur/e-compositeur/trice interprète": [
        "auteur-compositeur interprète",
        "auteure-compositrice interprète",
    ],
    # Cas avec reporter
    "reporter/trice-photographe": ["reporter-photographe", "reportrice-photographe"],
    # Cas avec enseignant/chercheur
    "enseignant/e-chercheur/euse": ["enseignant-chercheur", "enseignante-chercheuse"],
    # Cas avec expert
    "expert/e-comptable": ["expert-comptable", "experte-comptable"],
    # Cas spéciaux simples
    "hôte/esse d'accueil": ["hôte d'accueil", "hôtesse d'accueil"],
    "maçon/ne": ["maçon", "maçonne"],
    # Cas avec adjectifs
    "adjoint/e administratif/ve": ["adjoint administratif", "adjointe administrative"],
    "secrétaire administratif/ve": [
        "secrétaire administratif",
        "secrétaire administrative",
    ],
    "designer/euse industriel/le": ["designer industriel", "designeuse industrielle"],
    "éducateur/trice canin/ne": ["éducateur canin", "éducatrice canine"],
    "e-sportif/ve": ["e-sportif", "e-sportive"],
    # Cas avec BIM
    "technicien/ne BIM modeleu/euse": [
        "technicien BIM modeleur",
        "technicienne BIM modeleuse",
    ],
    # Cas avec slash spéciaux (non-genre)
    "femme / valet de chambre": ["femme de chambre", "valet de chambre"],
    "interprète français / LSF (langue des signes française)": [
        "interprète français / LSF (langue des signes française)"
    ],
    "gestionnaire actif/passif": ["gestionnaire actif/passif"],
    "responsable de bureau d'études et/ou des méthodes (textile)": [
        "responsable de bureau d'études et/ou des méthodes (textile)"
    ],
}


def expand_inclusive_word(word_with_slash):
    """
    Transforme un mot avec écriture inclusive en ses deux formes.

    Exemples:
      - "développeur/euse" → ("développeur", "développeuse")
      - "ingénieur/e" → ("ingénieur", "ingénieure")
      - "collaborateur/trice" → ("collaborateur", "collaboratrice")
      - "conseiller/ère" → ("conseiller", "conseillère")
      - "chef/fe" → ("chef", "cheffe")
    """
    if "/" not in word_with_slash:
        return (word_with_slash,)

    parts = word_with_slash.split("/")
    if len(parts) != 2:
        return (word_with_slash,)

    base, suffix = parts

    # Ignorer les cas qui ne sont pas du genre (et/ou, actif/passif, etc.)
    non_gender_patterns = ["et/ou", "actif/passif", "web/mobile", "net/mois", "lsf"]
    if word_with_slash.lower() in non_gender_patterns:
        return (word_with_slash,)

    # Ignorer les patterns avec espaces ou parenthèses (cas spéciaux)
    if " " in word_with_slash or "(" in word_with_slash:
        return (word_with_slash,)

    # Règles de transformation par ordre de spécificité

    # 0. Cas très spéciaux
    if base == "maître" and suffix == "esse":
        # maître/esse → maître, maîtresse
        masculine = "maître"
        feminine = "maîtresse"

    elif base.endswith("man") and suffix == "woman":
        # perchman/woman → perchman, perchwoman
        masculine = base
        feminine = base[:-3] + "woman"

    elif base == "préfet" and suffix == "ète":
        # préfet/ète → préfet, préfète
        masculine = base
        feminine = "préfète"

    elif base.endswith("eron") and suffix == "ne":
        # bûcheron/ne → bûcheron, bûcheronne
        masculine = base
        feminine = base[:-2] + "onne"

    elif base.endswith("ier") and suffix == "ière":
        # pâtissier/ière, kiosquier/ière → pâtissier/pâtissière
        masculine = base
        feminine = base[:-3] + "ière"

    elif base.endswith("é") and suffix == "ée":
        # délégué/ée → délégué, déléguée
        masculine = base
        feminine = base + "e"

    elif base == "sportif" and suffix == "ve":
        # sportif/ve → sportif, sportive
        masculine = base
        feminine = "sportive"

    elif base == "industriel" and suffix == "le":
        # industriel/le → industriel, industrielle
        masculine = base
        feminine = base + "le"

    # 1. Cas spéciaux avec terminaisons complexes
    elif base.endswith("teur") and suffix == "trice":
        # directeur/trice → directeur, directrice
        masculine = base
        feminine = base[:-4] + "trice"

    elif base.endswith("teur") and suffix == "rice":
        # éducateur/trice, mais écrit /rice → éducateur, éducatrice
        masculine = base
        feminine = base[:-4] + "trice"

    elif base.endswith("eur") and suffix == "rice":
        # acteur/rice → acteur, actrice
        masculine = base
        feminine = base[:-3] + "rice"

    elif base.endswith("eur") and suffix == "euse":
        # développeur/euse, vendeur/euse → développeur/développeuse
        masculine = base
        feminine = base[:-3] + "euse"

    elif base.endswith("eur") and suffix == "trice":
        # opérateur/trice → opérateur, opératrice
        masculine = base
        feminine = base[:-3] + "trice"

    # 2. Terminaisons en -ier/-ère
    elif base.endswith("ier") and suffix == "ère":
        # conseiller/ère, officier/ère → conseiller/conseillère
        masculine = base
        feminine = base[:-3] + "ère"

    elif base.endswith("er") and suffix == "ère":
        # boulanger/ère → boulanger, boulangère
        masculine = base
        feminine = base[:-2] + "ère"

    # 3. Terminaisons en -en/-enne
    elif base.endswith("ien") and suffix == "ne":
        # technicien/ne → technicien, technicienne
        masculine = base
        feminine = base[:-2] + "enne"

    elif base.endswith("cien") and suffix == "ne":
        # pharmacien/ne → pharmacien, pharmacienne
        masculine = base
        feminine = base[:-2] + "enne"

    elif base.endswith("en") and suffix == "ne":
        # gardien/ne → gardien, gardienne
        masculine = base
        feminine = base[:-2] + "enne"

    # 4. Terminaisons en -al/-ale
    elif base.endswith("al") and suffix == "ale":
        # territorial/ale, général/ale → territorial/territoriale
        masculine = base
        feminine = base + "e"

    # 5. Chef/cheffe (cas spécial)
    elif base == "chef" and suffix in ["fe", "fes"]:
        # chef/fe → chef, cheffe
        masculine = "chef"
        feminine = "cheffe"

    # 6. Terminaisons en -eur sans suffixe spécifique
    elif base.endswith("eur") and suffix == "e":
        # professeur/e → professeur, professeure
        masculine = base
        feminine = base + "e"

    # 7. Adjectifs en -if/-ive
    elif base.endswith("if") and suffix == "ive":
        # administratif/ive, éducatif/ive → administratif/administrative
        masculine = base
        feminine = base[:-2] + "ive"

    # 8. Adjectifs en -el/-elle
    elif base.endswith("el") and suffix == "le":
        # opérationnel/le → opérationnel, opérationnelle
        masculine = base
        feminine = base + "le"

    elif base.endswith("el") and suffix == "elle":
        # professionnel/elle → professionnel, professionnelle
        masculine = base
        feminine = base[:-2] + "elle"

    # 9. Terminaisons simples en /e
    elif suffix == "e" and not base.endswith("e"):
        # ingénieur/e, chargé/e, employé/e → + e
        masculine = base
        feminine = base + "e"

    # 10. Terminaisons en -ant/-ante
    elif base.endswith("ant") and suffix == "e":
        # accompagnant/e → accompagnant, accompagnante
        masculine = base
        feminine = base + "e"

    # 11. Cas complexes avec double terminaison
    elif base.endswith("ateur") and suffix == "trice":
        # administrateur/trice → administrateur, administratrice
        masculine = base
        feminine = base[:-4] + "trice"

    # 12. Autres cas en -eur générique
    elif base.endswith("eur") and len(suffix) > 0:
        # Essayer de deviner (dernier recours)
        masculine = base
        if suffix in ["euse", "rice", "trice"]:
            if suffix == "euse":
                feminine = base[:-3] + "euse"
            elif suffix in ["rice", "trice"]:
                feminine = base[:-3] + "trice"
            else:
                feminine = base + suffix
        else:
            feminine = base + suffix

    else:
        # Cas non géré, garder tel quel
        return (word_with_slash,)

    return (masculine, feminine)


def expand_inclusive_title(title):
    """
    Génère toutes les variantes d'un titre avec écriture inclusive.
    """
    # Trouver tous les mots avec /
    pattern = r"\S+/\S+"
    matches = list(re.finditer(pattern, title))

    if not matches:
        return [title]

    # Générer toutes les combinaisons
    def generate_combinations(text, match_index=0):
        if match_index >= len(matches):
            return [text]

        match = matches[match_index]
        word = match.group()
        variants = expand_inclusive_word(word)

        results = []
        for variant in variants:
            new_text = text[: match.start()] + variant + text[match.end() :]
            # Ajuster les positions des matches suivants
            offset = len(variant) - len(word)
            for m in matches[match_index + 1 :]:
                m.regs = ((m.start() + offset, m.end() + offset),)

            results.extend(generate_combinations(new_text, match_index + 1))

        return results

    # Approche simplifiée : traiter un mot à la fois récursivement
    def process_recursive(text):
        match = re.search(pattern, text)
        if not match:
            return [text]

        word = match.group()
        variants = expand_inclusive_word(word)

        results = []
        for variant in variants:
            new_text = text[: match.start()] + variant + text[match.end() :]
            results.extend(process_recursive(new_text))

        return results

    all_variants = process_recursive(title)

    # Dédupliquer et trier
    return sorted(list(set(all_variants)))


def normalize_title_simple(title):
    """
    Version simplifiée: remplace les formes inclusives par la version masculine uniquement.
    """
    result = title

    # Appliquer les règles dans l'ordre
    result = re.sub(r"(\w+)eur/euse\b", r"\1eur", result)
    result = re.sub(r"(\w+)teur/rice\b", r"\1teur", result)
    result = re.sub(r"(\w+)eur/rice\b", r"\1eur", result)
    result = re.sub(r"(\w+)ier/ère\b", r"\1ier", result)
    result = re.sub(r"(\w+)en/ne\b", r"\1en", result)
    result = re.sub(r"(\w+)al/ale\b", r"\1al", result)
    result = re.sub(r"(\w+)/e\b", r"\1", result)

    return result


def extract_all_variants(title):
    """
    Génère toutes les variantes utiles pour la recherche.
    Utilise d'abord le dictionnaire en dur, sinon applique les règles.
    """
    variants = set()

    # Titre original
    variants.add(title)

    # 1. Vérifier d'abord dans le dictionnaire en dur
    if title in HARDCODED_EXPANSIONS:
        variants.update(HARDCODED_EXPANSIONS[title])
        # Ajouter aussi la version sans slash
        variants.add(normalize_title_simple(title))
    else:
        # 2. Sinon, appliquer les règles automatiques
        # Version masculine simple
        variants.add(normalize_title_simple(title))

        # Toutes les combinaisons
        try:
            expanded = expand_inclusive_title(title)
            variants.update(expanded)
        except:
            # En cas d'erreur, au moins garder les versions de base
            pass

    # Nettoyer et trier
    result = sorted([v for v in variants if v.strip()])
    return result


def process_metier_file(filepath):
    """
    Traite un fichier de métier et extrait les variantes de titre.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Extraire le titre (première ligne après le #)
    lines = content.split("\n")
    title_line = None

    for line in lines:
        if line.startswith("# "):
            title_line = line[2:].strip()
            break

    if not title_line:
        return None

    # Générer les variantes
    variants = extract_all_variants(title_line)

    # Extraire l'ID du métier
    metier_id = None
    for line in lines:
        if line.startswith("**ID:**"):
            metier_id = line.replace("**ID:**", "").strip()
            break

    return {
        "file": filepath.name,
        "original_title": title_line,
        "metier_id": metier_id,
        "variants": variants,
        "variant_count": len(variants),
    }


def add_search_keywords_to_file(filepath, variants, metier_id):
    """
    Ajoute un paragraphe de mots-clés cachés à la fin du fichier pour améliorer la recherche.
    Alternative au frontmatter YAML qui peut poser problème selon le parser Markdown.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Vérifier si les mots-clés existent déjà
    if "<!-- SEARCH_KEYWORDS" in content:
        return False

    # Créer la section de mots-clés (en commentaire HTML pour ne pas être visible)
    keywords_section = "\n\n<!-- SEARCH_KEYWORDS\n"
    keywords_section += f"Variantes du titre (pour recherche):\n"
    for variant in variants:
        keywords_section += f"- {variant}\n"
    keywords_section += "-->\n"

    # Ajouter à la fin
    new_content = content.rstrip() + keywords_section

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True


def main():
    """
    Analyse tous les fichiers de métiers et affiche/ajoute les variantes de titres.
    """
    metiers_dir = Path("output/metiers")

    if not metiers_dir.exists():
        print(f"❌ Dossier {metiers_dir} non trouvé")
        return

    print("═" * 70)
    print("🔍 NORMALISATION DES TITRES DE MÉTIERS POUR RAG")
    print("═" * 70)
    print()

    # Collecter les statistiques
    all_results = []
    problematic_titles = []

    for filepath in sorted(metiers_dir.glob("*.md")):
        result = process_metier_file(filepath)
        if result:
            all_results.append(result)

            # Détecter les titres problématiques (avec écriture inclusive)
            if "/" in result["original_title"]:
                problematic_titles.append(result)

    print(f"📊 STATISTIQUES")
    print(f"   Fichiers analysés      : {len(all_results)}")
    print(f"   Titres avec / (inclus) : {len(problematic_titles)}")
    print(
        f"   Pourcentage            : {len(problematic_titles) * 100 // len(all_results)}%"
    )
    print()

    if problematic_titles:
        print("=" * 70)
        print("📝 EXEMPLES DE TITRES ET LEURS VARIANTES DE RECHERCHE")
        print("=" * 70)
        print()

        # Afficher quelques exemples représentatifs
        examples = [
            "développeur/euse",
            "ingénieur/e",
            "collaborateur/trice",
            "conseiller/ère",
            "technicien/ne",
        ]

        shown = 0
        for pattern in examples:
            for result in problematic_titles:
                if pattern in result["original_title"].lower() and shown < 15:
                    print(f"✓ {result['original_title']}")
                    print(f"  ID: {result['metier_id']}")
                    print(f"  Variantes:")
                    for variant in result["variants"]:
                        marker = "  " if variant == result["original_title"] else "→ "
                        print(f"     {marker}{variant}")
                    print()
                    shown += 1
                    break
            if shown >= 15:
                break

    print("=" * 70)
    print("💡 SOLUTION PROPOSÉE")
    print("=" * 70)
    print()
    print("Pour résoudre le problème de recherche dans RagFlow:")
    print()
    print("1. Ajouter les variantes dans les fichiers Markdown")
    print("   (en commentaire HTML invisible)")
    print()
    print("2. RagFlow indexera automatiquement ces variantes")
    print()
    print("3. Recherches qui fonctionneront:")
    print("   - 'développeur rural' → trouvera 'développeur/euse rural/e'")
    print("   - 'développeuse rurale' → trouvera 'développeur/euse rural/e'")
    print("   - 'ingénieure' → trouvera 'ingénieur/e'")
    print()
    response = input("Ajouter les variantes aux fichiers ? [o/N] : ").strip().lower()

    if response in ["o", "oui", "y", "yes"]:
        print()
        print("🚀 Ajout des variantes de recherche...")
        print()

        added_count = 0
        for result in all_results:
            if "/" in result["original_title"]:  # Seulement pour les titres inclusifs
                filepath = metiers_dir / result["file"]
                if add_search_keywords_to_file(
                    filepath, result["variants"], result["metier_id"]
                ):
                    added_count += 1
                    if added_count % 100 == 0:
                        print(f"   ✓ {added_count} fichiers traités...")

        print()
        print(f"✅ Variantes ajoutées à {added_count} fichiers")
        print()
        print("📋 Prochaines étapes:")
        print("   1. Réimporter les fichiers dans RagFlow")
        print("   2. Les recherches trouveront maintenant toutes les variantes")
    else:
        print()
        print("ℹ️  Aucune modification apportée aux fichiers")

    print()
    print("=" * 70)
    print("✨ ANALYSE TERMINÉE")
    print("=" * 70)


if __name__ == "__main__":
    main()
