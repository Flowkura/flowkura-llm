#!/usr/bin/env python3
"""
Script universel de conversion XML → Markdown pour tous les fichiers ONISEP/IDEO.
La configuration est externalisée dans config.toml

Usage:
    python convert_xml_to_markdown.py              # Convertit TOUT
    python convert_xml_to_markdown.py formations    # Seulement les formations détaillées
    python convert_xml_to_markdown.py metiers       # Seulement les métiers détaillés
    python convert_xml_to_markdown.py --help        # Aide
"""

import xml.etree.ElementTree as ET
import re
from pathlib import Path
from html import unescape
import sys
import time
from glob import glob

# Lecture de la configuration depuis config.toml
try:
    import tomllib
except ImportError:
    import tomli as tomllib


# ============================================================================
# CHARGEMENT DE LA CONFIGURATION
# ============================================================================


def load_config():
    """Charge la configuration depuis config.toml"""
    config_file = Path("config.toml")
    if not config_file.exists():
        print("❌ Fichier config.toml non trouvé!")
        sys.exit(1)

    with open(config_file, "rb") as f:
        return tomllib.load(f)


CONVERSIONS = load_config()["conversions"]


# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================


def clean_html(html_text):
    """Nettoie le texte HTML en Markdown."""
    if not html_text:
        return ""

    text = unescape(html_text)
    text = re.sub(r"<h5>(.*?)</h5>", r"### \1", text, flags=re.DOTALL)
    text = re.sub(r"<h4>(.*?)</h4>", r"## \1", text, flags=re.DOTALL)
    text = re.sub(r"<h3>(.*?)</h3>", r"## \1", text, flags=re.DOTALL)
    text = re.sub(r"<p>(.*?)</p>", r"\1\n", text, flags=re.DOTALL)
    text = re.sub(r"<strong>(.*?)</strong>", r"**\1**", text, flags=re.DOTALL)
    text = re.sub(r"<em>(.*?)</em>", r"*\1*", text, flags=re.DOTALL)
    text = re.sub(r"<ul>", "", text)
    text = re.sub(r"</ul>", "", text)
    text = re.sub(r"<li>(.*?)</li>", r"- \1\n", text, flags=re.DOTALL)
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\n\s*\n\s*\n", "\n\n", text)
    return text.strip()


def get_text(element, tag, default=""):
    """Récupère le texte d'un élément XML."""
    child = element.find(tag)
    if child is not None and child.text:
        return unescape(child.text.strip())
    return default


def get_cdata_text(element, tag, default=""):
    """Récupère le texte CDATA d'un élément XML."""
    return get_text(element, tag, default)


def safe_filename(text, index):
    """Crée un nom de fichier sûr."""
    safe = re.sub(r"[^\w\s-]", "", text.lower())
    safe = re.sub(r"[-\s/]+", "_", safe)
    return f"item_{index:06d}_{safe[:100]}.md"


# ============================================================================
# CONVERTISSEURS SPÉCIALISÉS
# ============================================================================


def convert_formation_detaillee(formation):
    """Convertit une fiche formation ONISEP détaillée."""
    identifiant = get_text(formation, "identifiant")
    libelle = get_text(formation, "libelle_complet")
    if not libelle:
        return None, None

    md = [f"# {libelle}\n\n## Informations générales\n\n"]

    # Métadonnées
    for field, label in [
        ("code_scolarite", "Code scolarité"),
        ("sigle", "Sigle"),
        ("duree_formation", "Durée"),
        ("niveau_certification", "Niveau de certification"),
    ]:
        val = get_text(formation, field)
        if val:
            cleaned_val = val.strip('"')
            md.append(f"**{label}:** {cleaned_val}\n")

    # Type de formation
    type_elem = formation.find("type_Formation")
    if type_elem is not None:
        type_lib = get_text(type_elem, "type_formation_libelle")
        type_sig = get_text(type_elem, "type_formation_sigle")
        if type_lib:
            md.append(
                f"**Type:** {type_lib}" + (f" ({type_sig})" if type_sig else "") + "\n"
            )

    # URL
    url = get_text(formation, "url")
    if url:
        md.append(f"\n**Lien:** [{url}]({url})\n")

    # Descriptifs
    for field, title in [
        ("descriptif_format_court", "Description"),
        ("descriptif_acces", "Accès"),
        ("attendus", "Attendus"),
        ("descriptif_poursuite_etudes", "Poursuite d'études"),
    ]:
        text = get_text(formation, field)
        if text:
            cleaned = clean_html(text)
            if cleaned:
                md.append(f"\n## {title}\n\n{cleaned}\n")

    # Métiers associés
    metiers = formation.findall(".//metier")
    if metiers:
        md.append("\n## Métiers associés\n\n")
        for metier in metiers[:10]:
            nom = get_text(metier, "nom_metier")
            if nom:
                md.append(f"- {nom}\n")

    safe_name = re.sub(r"[^\w\s-]", "", libelle.lower())
    safe_name = re.sub(r"[-\s]+", "_", safe_name)[:100]
    return "".join(md), f"{identifiant}_{safe_name}.md"


def convert_metier_detaille(metier):
    """Convertit une fiche métier ONISEP détaillée."""
    identifiant = get_text(metier, "identifiant")
    nom = get_text(metier, "nom_metier")
    if not nom:
        return None, None

    md = [f"# {nom}\n\n**ID:** {identifiant}\n"]

    # Codes ROME
    romes = metier.findall(".//romeV3")
    if romes:
        md.append(
            "\n**Codes ROME:** "
            + ", ".join(r.text.strip() for r in romes if r.text)
            + "\n"
        )

    # Sections CDATA
    for field, title in [
        ("accroche_metier", "Présentation"),
        ("format_court", "En bref"),
        ("nature_travail", "Nature du travail"),
        ("competences", "Compétences requises"),
        ("condition_travail", "Conditions de travail"),
        ("vie_professionnelle", "Vie professionnelle"),
        ("acces_metier", "Accès au métier"),
    ]:
        text = get_cdata_text(metier, field)
        if text:
            cleaned = clean_html(text)
            if cleaned:
                md.append(f"\n## {title}\n\n{cleaned}\n")

    # Formations recommandées
    formations = metier.findall(".//formation_min_requise")
    if formations:
        md.append("\n## Formations recommandées\n\n")
        for form in formations[:15]:
            lib = get_text(form, "libelle")
            if lib:
                md.append(f"- {lib}\n")

    safe_name = re.sub(r"[^\w\s-]", "", nom.lower())
    safe_name = re.sub(r"[-\s/]+", "_", safe_name)[:100]
    return "".join(md), f"{identifiant}_{safe_name}.md"


def convert_formation_ideo(item, index):
    """Convertit une formation IDEO (référentiel)."""
    libelle = get_text(item, "libelle_formation_principal")
    if not libelle:
        return None, None

    md = [f"# {libelle}\n\n## Informations\n\n"]

    for field, label in [
        ("libelle_type_formation", "Type"),
        ("sigle_type_formation", "Sigle type"),
        ("sigle_formation", "Sigle"),
        ("duree", "Durée"),
        ("niveau_de_sortie_indicatif", "Niveau sortie"),
        ("code_rncp", "Code RNCP"),
        ("libelle_niveau_de_certification", "Certification"),
        ("code_scolarite", "Code scolarité"),
        ("code_nsf", "Code NSF"),
        ("tutelle", "Tutelle"),
    ]:
        val = get_text(item, field)
        if val and val != "non renseigné":
            md.append(f"**{label}:** {val}\n")

    url = get_text(item, "url_et_id_onisep")
    if url:
        md.append(f"\n**Lien:** [{url}]({url})\n")

    return "".join(md), safe_filename(libelle, index)


def convert_metier_ideo(item, index):
    """Convertit un métier IDEO (référentiel)."""
    libelle = get_text(item, "libelle_metier")
    if not libelle:
        return None, None

    md = [f"# {libelle}\n\n"]

    lien = get_text(item, "lien_site_onisepfr")
    if lien:
        md.append(f"**Lien:** [{lien}]({lien})\n")

    for field, label in [
        ("nom_publication", "Publication"),
        ("collection", "Collection"),
        ("annee", "Année"),
        ("gfe", "GFE"),
        ("code_rome", "Code ROME"),
        ("libelle_rome", "ROME"),
    ]:
        val = get_text(item, field)
        if val:
            md.append(f"**{label}:** {val}\n")

    return "".join(md), safe_filename(libelle, index)


def convert_generic(item, index):
    """Convertisseur générique pour les autres fichiers."""
    title = None
    for child in item:
        if child.text and len(child.text.strip()) > 3:
            title = child.text.strip()
            break

    if not title:
        return None, None

    md = [f"# {title}\n\n"]

    for child in item:
        if child.text and child.text.strip():
            val = unescape(child.text.strip())
            tag = child.tag.replace("_", " ").title()

            if "url" in child.tag.lower() or "lien" in child.tag.lower():
                md.append(f"**{tag}:** [{val}]({val})\n")
            else:
                md.append(f"**{tag}:** {val}\n")

    return "".join(md), safe_filename(title, index)


# ============================================================================
# MOTEUR DE CONVERSION
# ============================================================================


def convert_file(key, config):
    """Convertit un fichier XML en Markdown."""
    xml_pattern = config["file"]
    output_dir = Path(config["output"])
    conv_type = config["type"]
    desc = config["description"]

    print(f"\n{'=' * 70}")
    print(f"📄 {desc}")
    print(f"{'=' * 70}")

    # Support des wildcards (fichiers découpés)
    xml_files = glob(xml_pattern) if "*" in xml_pattern else [xml_pattern]

    if not xml_files:
        print(f"⚠️  Aucun fichier trouvé: {xml_pattern}")
        return 0

    if len(xml_files) > 1:
        print(f"📦 Fichiers découpés trouvés: {len(xml_files)}")
        for f in xml_files:
            print(f"   - {Path(f).name}")

    output_dir.mkdir(parents=True, exist_ok=True)

    all_items = []

    # Traiter tous les fichiers (parties découpées)
    for xml_file in sorted(xml_files):
        if not Path(xml_file).exists():
            print(f"⚠️  Fichier non trouvé: {xml_file}")
            continue

        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            # Sélectionner les éléments à convertir
            if conv_type in ["formations_detaillees", "metiers_detailles"]:
                items = (
                    root.findall(".//formation")
                    if conv_type == "formations_detaillees"
                    else root.findall(".//metier")
                )
            else:
                items = root.findall(".//item")

            all_items.extend(items)
        except Exception as e:
            print(f"❌ Erreur lecture {xml_file}: {e}")
            continue

    total = len(all_items)
    print(f"Items trouvés: {total}")

    # Choisir le convertisseur
    converters = {
        "formations_detaillees": convert_formation_detaillee,
        "metiers_detailles": convert_metier_detaille,
        "formations_ideo": convert_formation_ideo,
        "metiers_ideo": convert_metier_ideo,
        "generic": convert_generic,
    }
    converter = converters[conv_type]

    # Convertir tous les items
    converted = 0
    for idx, item in enumerate(all_items, 1):
        try:
            if conv_type in ["formations_ideo", "metiers_ideo", "generic"]:
                md_content, filename = converter(item, idx)
            else:
                md_content, filename = converter(item)

            if md_content and filename:
                filepath = output_dir / filename
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(md_content)
                converted += 1

            if idx % 500 == 0:
                print(f"  Progression: {idx}/{total}")
        except Exception as e:
            print(f"  Erreur item {idx}: {e}")
            continue

    print(f"✅ Terminé: {converted}/{total} fichiers")
    return converted


# ============================================================================
# MAIN
# ============================================================================


def main():
    """Fonction principale."""
    args = sys.argv[1:]

    # Aide
    if "--help" in args or "-h" in args:
        print(__doc__)
        print("\nCatégories disponibles:")
        for key, conf in CONVERSIONS.items():
            print(f"  {key:25} {conf['description']}")
        return

    print("═" * 70)
    print("🚀 CONVERSION XML → MARKDOWN - ONISEP/IDEO")
    print("═" * 70)

    start_time = time.time()

    # Déterminer quoi convertir
    if args:
        to_convert = {
            k: v for k, v in CONVERSIONS.items() if any(arg in k for arg in args)
        }
        if not to_convert:
            print(f"❌ Catégorie inconnue: {args}")
            print("Utilisez --help pour voir les catégories disponibles")
            return
    else:
        to_convert = CONVERSIONS

    # Conversion
    total_files = 0
    for key, config in to_convert.items():
        total_files += convert_file(key, config)

    # Statistiques
    duration = time.time() - start_time
    minutes = int(duration // 60)
    seconds = int(duration % 60)

    print(f"\n{'═' * 70}")
    print("✨ CONVERSION TERMINÉE!")
    print(f"{'═' * 70}")
    print(f"⏱️  Temps: {minutes}m {seconds}s")
    print(f"📦 Total: {total_files} fichiers Markdown générés")
    print(f"📁 Dossier: output/")
    print("🎯 Prêt pour RagFlow!")
    print("═" * 70)


if __name__ == "__main__":
    main()
