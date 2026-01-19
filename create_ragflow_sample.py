#!/usr/bin/env python3
"""
Création d'un échantillon RagFlow cohérent.
Approche: Sélectionner des formations variées et extraire tout ce qui est lié.
"""

import re
import shutil
from pathlib import Path
from collections import defaultdict

# Formations sélectionnées (codes réels vérifiés avec nombreuses actions)
SELECTED_FORMATIONS = [
    # Niveau lycée (bac général et bac pro)
    "3354",  # Bac général (2446 actions lycée)
    "5839",  # Bac pro métiers du commerce option A (825 actions)
    "4284",  # Bac pro assistance à la gestion (725 actions)
    "9919",  # Bac pro métiers de l'électricité (601 actions)
    "7562",  # Bac pro accompagnement soins et services (565 actions)
    # Niveau Bac+2 (BTS variés)
    "2317",  # BTS management commercial opérationnel (500 actions sup)
    "10529",  # BTS comptabilité et gestion (420 actions sup)
    "270",  # BTS gestion de la PME (392 actions sup)
    "269",  # BTS électrotechnique (177 actions sup)
    "5337",  # BTS services informatiques option SISR (239 actions)
    # Niveau Bac+3+
    "351",  # Diplôme de comptabilité et gestion (157 actions)
    "2378",  # Diplôme d'État d'infirmier (343 actions)
]


def extract_formation_code(formation_file):
    """Extrait le code FOR d'un fichier de formation."""
    # Le code est dans le nom du fichier: FOR.xxxx_nom.md
    match = re.search(r"FOR\.(\d+)", formation_file.name)
    return match.group(1) if match else None


def find_formation_file_by_code(formations_dir, form_code):
    """Trouve le fichier de formation par son code."""
    for form_file in formations_dir.glob(f"FOR.{form_code}_*.md"):
        return form_file
    return None


def find_actions_for_formation(actions_dirs, form_code):
    """Trouve les actions de formation qui référencent ce code FOR."""
    found = []

    for actions_dir in actions_dirs:
        if not actions_dir.exists():
            continue

        for action_file in actions_dir.glob("*.md"):
            content = action_file.read_text(encoding="utf-8")

            # Chercher le code FOR.xxxx dans le contenu
            if f"FOR.{form_code}" in content or f"FOR/{form_code}" in content:
                found.append(action_file)

                if len(found) >= 15:  # Limiter pour l'échantillon
                    return found

    return found


def extract_action_info(action_file):
    """Extrait les infos d'une action."""
    content = action_file.read_text(encoding="utf-8")

    # Codes UAI des établissements
    codes_uai = set(re.findall(r"Ens Code Uai:\*\*\s*(\w+)", content))

    # Région
    region_match = re.search(r"Ens Region:\*\*\s*(.+)$", content, re.MULTILINE)
    region = region_match.group(1).strip() if region_match else None

    # Ville
    ville_match = re.search(r"Ens Commune:\*\*\s*(.+)$", content, re.MULTILINE)
    ville = ville_match.group(1).strip() if ville_match else None

    # Nom établissement
    nom_match = re.search(
        r"Lieu Denseignement Ens Libelle:\*\*\s*(.+)$", content, re.MULTILINE
    )
    nom = nom_match.group(1).strip() if nom_match else None

    return {
        "codes_uai": list(codes_uai),
        "region": region,
        "ville": ville,
        "nom_etablissement": nom,
    }


def find_etablissement_by_uai(structures_dirs, code_uai):
    """Trouve un établissement par son code UAI."""
    for structures_dir in structures_dirs:
        if not structures_dir.exists():
            continue

        for etab_file in structures_dir.glob("*.md"):
            if (
                code_uai in etab_file.name
                or code_uai in etab_file.read_text(encoding="utf-8")[:500]
            ):
                return etab_file

    return None


def find_related_metiers(metiers_dir, keywords):
    """Trouve des métiers liés par mots-clés."""
    found = []

    # Mots-clés significatifs (> 4 caractères)
    keywords = [k.lower() for k in keywords if len(k) > 4][:3]

    if not keywords:
        return found

    for metier_file in metiers_dir.glob("*.md"):
        content_lower = metier_file.read_text(encoding="utf-8").lower()

        # Chercher si au moins un mot-clé est présent
        if any(kw in content_lower for kw in keywords):
            found.append(metier_file)

            if len(found) >= 3:  # Limiter à 3 métiers par formation
                break

    return found


def main():
    """Crée l'échantillon RagFlow."""
    output_dir = Path("output")
    sample_dir = Path("ragflow-sample")

    # Nettoyer et créer la structure
    if sample_dir.exists():
        shutil.rmtree(sample_dir)

    sample_dir.mkdir(exist_ok=True)
    (sample_dir / "1_metiers").mkdir(exist_ok=True)
    (sample_dir / "2_formations").mkdir(exist_ok=True)
    (sample_dir / "3_actions_formation").mkdir(exist_ok=True)
    (sample_dir / "4_etablissements").mkdir(exist_ok=True)

    print("=" * 70)
    print("🎯 CRÉATION ÉCHANTILLON RAGFLOW")
    print("=" * 70)
    print()

    formations_dir = output_dir / "formations"
    actions_dirs = [
        output_dir / "ideo_actions_college",
        output_dir / "ideo_actions_lycee",
        output_dir / "ideo_actions_superieur",
    ]
    structures_dirs = [
        output_dir / "ideo_structures_secondaire",
        output_dir / "ideo_structures_superieur",
    ]
    metiers_dir = output_dir / "metiers"

    total_actions = 0
    total_etablissements = 0
    total_metiers = 0
    regions_coverage = set()
    copied_metiers = set()

    # Traiter chaque formation sélectionnée
    for idx, form_code in enumerate(SELECTED_FORMATIONS, 1):
        print(f"\n{'=' * 70}")
        print(f"📚 Formation {idx}/{len(SELECTED_FORMATIONS)}: FOR.{form_code}")
        print(f"{'=' * 70}")

        # 1. Copier la formation
        form_file = find_formation_file_by_code(formations_dir, form_code)
        if not form_file:
            print(f"  ⚠️  Fichier formation non trouvé")
            continue

        shutil.copy2(form_file, sample_dir / "2_formations" / form_file.name)
        print(f"  ✓ Formation: {form_file.name}")

        # Extraire le nom pour chercher les métiers liés
        form_name = form_file.stem.replace(f"FOR.{form_code}_", "").replace("_", " ")
        keywords = form_name.split()

        # 2. Trouver et copier les actions liées
        print(f"\n  🎓 Actions de formation:")
        actions = find_actions_for_formation(actions_dirs, form_code)

        if not actions:
            print(f"     Aucune action trouvée")
            continue

        for action_file in actions[:10]:  # Max 10 par formation
            info = extract_action_info(action_file)

            # Copier l'action
            shutil.copy2(
                action_file, sample_dir / "3_actions_formation" / action_file.name
            )
            total_actions += 1

            if info["region"]:
                regions_coverage.add(info["region"])

            print(
                f"     ✓ {info['nom_etablissement'][:45]:45} ({info['ville']}, {info['region']})"
            )

            # 3. Trouver et copier l'établissement
            for code_uai in info["codes_uai"][
                :1
            ]:  # Un seul établissement par action pour l'échantillon
                etab_file = find_etablissement_by_uai(structures_dirs, code_uai)
                if etab_file:
                    dest = sample_dir / "4_etablissements" / etab_file.name
                    if not dest.exists():
                        shutil.copy2(etab_file, dest)
                        total_etablissements += 1

        # 4. Trouver et copier les métiers liés
        print(f"\n  👤 Métiers liés:")
        metiers = find_related_metiers(metiers_dir, keywords)

        for metier_file in metiers:
            if metier_file.name not in copied_metiers:
                shutil.copy2(metier_file, sample_dir / "1_metiers" / metier_file.name)
                copied_metiers.add(metier_file.name)
                total_metiers += 1

                # Extraire le titre
                content = metier_file.read_text(encoding="utf-8")
                first_line = content.split("\n")[0].replace("# ", "")
                print(f"     ✓ {first_line[:60]}")

    # Statistiques finales
    print()
    print("=" * 70)
    print("✨ ÉCHANTILLON CRÉÉ")
    print("=" * 70)
    print()
    print(f"📁 Dossier: ragflow-sample/")
    print(f"   ├─ 1_metiers/              : {total_metiers} fichiers")
    print(f"   ├─ 2_formations/           : {len(SELECTED_FORMATIONS)} fichiers")
    print(f"   ├─ 3_actions_formation/    : {total_actions} fichiers")
    print(f"   └─ 4_etablissements/       : {total_etablissements} fichiers")
    print()
    print(
        f"📊 Total: {total_metiers + len(SELECTED_FORMATIONS) + total_actions + total_etablissements} fichiers"
    )
    print(f"🌍 Couverture régionale: {len(regions_coverage)} régions")
    if regions_coverage:
        print(f"   {', '.join(sorted(regions_coverage)[:5])}")
    print()
    print("🎯 Parcours complet testable:")
    print("   Métier → Formation → Actions → Établissements → Localisation")
    print()


if __name__ == "__main__":
    main()
