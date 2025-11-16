#!/usr/bin/env python3
"""
Script pour découper les gros fichiers XML en morceaux < 50 MB.
Respecte la structure XML pour garantir la validité de chaque partie.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import os


def get_file_size_mb(filepath):
    """Retourne la taille en MB."""
    return os.path.getsize(filepath) / (1024 * 1024)


def split_xml_file(input_file, max_size_mb=45):
    """
    Découpe un fichier XML en plusieurs parties < max_size_mb.
    Chaque partie est un XML valide.
    """
    input_path = Path(input_file)
    current_size = get_file_size_mb(input_file)
    
    if current_size <= 50:
        print(f"✅ {input_path.name}: {current_size:.1f} MB - OK, pas besoin de découper")
        return []
    
    print(f"📄 {input_path.name}: {current_size:.1f} MB - Découpage nécessaire")
    
    # Parser le XML
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    # Compter les items
    items = root.findall('.//item')
    total_items = len(items)
    
    if total_items == 0:
        print(f"  ⚠️  Aucun item trouvé, impossible de découper")
        return []
    
    print(f"  Items trouvés: {total_items}")
    
    # Calculer le nombre de parties nécessaires
    num_parts = int(current_size / max_size_mb) + 1
    items_per_part = total_items // num_parts + 1
    
    print(f"  Parties à créer: {num_parts}")
    print(f"  Items par partie: ~{items_per_part}")
    
    # Créer les parties
    output_files = []
    base_name = input_path.stem
    
    for part_num in range(num_parts):
        start_idx = part_num * items_per_part
        end_idx = min((part_num + 1) * items_per_part, total_items)
        
        if start_idx >= total_items:
            break
        
        # Créer un nouveau XML pour cette partie
        new_root = ET.Element(root.tag)
        new_root.attrib.update(root.attrib)
        
        # Copier les items de cette partie
        for item in items[start_idx:end_idx]:
            new_root.append(item)
        
        # Créer le fichier
        output_filename = f"{base_name}_part{part_num+1:02d}.xml"
        output_path = input_path.parent / output_filename
        
        new_tree = ET.ElementTree(new_root)
        ET.indent(new_tree, space="  ")
        new_tree.write(output_path, encoding='utf-8', xml_declaration=True)
        
        size_mb = get_file_size_mb(output_path)
        items_count = len(new_root.findall('.//item'))
        
        print(f"  ✅ Créé: {output_filename} ({size_mb:.1f} MB, {items_count} items)")
        output_files.append(str(output_path))
    
    return output_files


def main():
    """Fonction principale."""
    print("═" * 70)
    print("🔪 DÉCOUPAGE DES GROS FICHIERS XML (> 50 MB)")
    print("═" * 70)
    print()
    
    files_dir = Path("files")
    
    if not files_dir.exists():
        print("❌ Dossier 'files/' non trouvé")
        return
    
    # Trouver tous les fichiers XML
    xml_files = list(files_dir.glob("*.xml"))
    
    print(f"📁 Fichiers XML trouvés: {len(xml_files)}")
    print()
    
    # Traiter chaque fichier
    all_parts = []
    files_to_split = []
    
    for xml_file in sorted(xml_files):
        size_mb = get_file_size_mb(xml_file)
        
        if size_mb > 50:
            files_to_split.append(xml_file)
            parts = split_xml_file(xml_file, max_size_mb=45)
            all_parts.extend(parts)
            print()
        else:
            print(f"✅ {xml_file.name}: {size_mb:.1f} MB - OK")
    
    # Résumé
    print()
    print("═" * 70)
    print("✨ RÉSUMÉ")
    print("═" * 70)
    
    if files_to_split:
        print(f"📊 Fichiers découpés: {len(files_to_split)}")
        print(f"📦 Parties créées: {len(all_parts)}")
        print()
        print("⚠️  IMPORTANT:")
        print("  1. Les fichiers originaux sont conservés")
        print("  2. Ajoutez les parties découpées à Git:")
        print("     git add files/*_part*.xml")
        print("  3. Optionnel: Supprimez les originaux > 50MB du repo:")
        for f in files_to_split:
            print(f"     git rm {f}")
        print("  4. Committez:")
        print("     git commit -m 'Fichiers XML découpés en parties < 50MB'")
        print("     git push")
    else:
        print("✅ Aucun fichier > 50 MB, tout est OK !")
    
    print()
    print("═" * 70)


if __name__ == "__main__":
    main()
