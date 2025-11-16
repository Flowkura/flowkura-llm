#!/usr/bin/env python3
"""
Script de détection et analyse des fichiers XML.
Aide à configurer config.toml en détectant les nouveaux fichiers,
analysant leur structure, et suggérant la configuration.

Maintient une base SQLite pour tracker les fichiers connus.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import sqlite3
import hashlib
import os
from datetime import datetime


# ============================================================================
# BASE DE DONNÉES
# ============================================================================

def init_database():
    """Initialise la base de données SQLite."""
    db_path = Path("files_tracking.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS xml_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE NOT NULL,
            filepath TEXT NOT NULL,
            filesize_mb REAL,
            file_hash TEXT,
            root_tag TEXT,
            item_count INTEGER,
            sample_tags TEXT,
            first_seen TEXT,
            last_seen TEXT,
            configured BOOLEAN DEFAULT 0,
            notes TEXT
        )
    """)
    
    conn.commit()
    return conn


def calculate_hash(filepath):
    """Calcule le hash MD5 d'un fichier."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_file_size_mb(filepath):
    """Retourne la taille en MB."""
    return os.path.getsize(filepath) / (1024 * 1024)


def analyze_xml_structure(filepath):
    """Analyse la structure d'un fichier XML."""
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        # Compter les items
        items = root.findall('.//item')
        if not items:
            items = root.findall('.//formation')
        if not items:
            items = root.findall('.//metier')
        
        item_count = len(items)
        
        # Récupérer des tags d'exemple du premier item
        sample_tags = []
        if items:
            first_item = items[0]
            sample_tags = [child.tag for child in first_item[:10]]  # 10 premiers tags
        
        return {
            'root_tag': root.tag,
            'item_count': item_count,
            'sample_tags': ', '.join(sample_tags[:10])
        }
    except Exception as e:
        return {
            'root_tag': 'ERROR',
            'item_count': 0,
            'sample_tags': f'Erreur: {str(e)}'
        }


# ============================================================================
# DÉTECTION DES FICHIERS
# ============================================================================

def scan_files(conn):
    """Scanne le dossier files/ et détecte les nouveaux fichiers."""
    files_dir = Path("files")
    
    if not files_dir.exists():
        print("❌ Dossier files/ non trouvé")
        return
    
    # Récupérer les fichiers existants en base
    cursor = conn.cursor()
    cursor.execute("SELECT filename, file_hash FROM xml_files")
    known_files = {row[0]: row[1] for row in cursor.fetchall()}
    
    # Scanner tous les fichiers XML
    xml_files = list(files_dir.glob("*.xml"))
    
    new_files = []
    modified_files = []
    unchanged_files = []
    
    for xml_file in sorted(xml_files):
        filename = xml_file.name
        filepath = str(xml_file)
        file_hash = calculate_hash(filepath)
        
        if filename not in known_files:
            # Nouveau fichier
            new_files.append(xml_file)
            
            # Analyser et ajouter en base
            size_mb = get_file_size_mb(filepath)
            analysis = analyze_xml_structure(filepath)
            now = datetime.now().isoformat()
            
            cursor.execute("""
                INSERT INTO xml_files 
                (filename, filepath, filesize_mb, file_hash, root_tag, 
                 item_count, sample_tags, first_seen, last_seen, configured)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
            """, (filename, filepath, size_mb, file_hash, 
                  analysis['root_tag'], analysis['item_count'], 
                  analysis['sample_tags'], now, now))
            
        elif known_files[filename] != file_hash:
            # Fichier modifié
            modified_files.append(xml_file)
            
            # Mettre à jour en base
            size_mb = get_file_size_mb(filepath)
            analysis = analyze_xml_structure(filepath)
            now = datetime.now().isoformat()
            
            cursor.execute("""
                UPDATE xml_files 
                SET filesize_mb = ?, file_hash = ?, root_tag = ?,
                    item_count = ?, sample_tags = ?, last_seen = ?
                WHERE filename = ?
            """, (size_mb, file_hash, analysis['root_tag'],
                  analysis['item_count'], analysis['sample_tags'], now, filename))
        else:
            # Fichier inchangé
            unchanged_files.append(xml_file)
    
    conn.commit()
    
    return {
        'new': new_files,
        'modified': modified_files,
        'unchanged': unchanged_files,
        'total': len(xml_files)
    }


# ============================================================================
# ANALYSE ET SUGGESTIONS
# ============================================================================

def suggest_config_for_file(cursor, filename):
    """Suggère une configuration pour un fichier."""
    cursor.execute("""
        SELECT filename, filesize_mb, root_tag, item_count, sample_tags
        FROM xml_files WHERE filename = ?
    """, (filename,))
    
    row = cursor.fetchone()
    if not row:
        return None
    
    filename, size_mb, root_tag, item_count, sample_tags = row
    
    suggestions = {
        'filename': filename,
        'size_mb': size_mb,
        'needs_split': size_mb > 50,
        'item_count': item_count,
        'config_key': '',
        'output_dir': '',
        'type': 'generic',
        'description': '',
        'file_pattern': '',
        'notes': []
    }
    
    # Détecter le type de fichier
    name_lower = filename.lower()
    
    # ONISEP détaillé
    if 'onisep_ideo_fiches_formations' in name_lower:
        suggestions['config_key'] = 'formations_onisep'
        suggestions['output_dir'] = 'output/formations'
        suggestions['type'] = 'formations_detaillees'
        suggestions['description'] = 'Fiches formations ONISEP détaillées'
    elif 'onisep_ideo_fiches_metiers' in name_lower:
        suggestions['config_key'] = 'metiers_onisep'
        suggestions['output_dir'] = 'output/metiers'
        suggestions['type'] = 'metiers_detailles'
        suggestions['description'] = 'Fiches métiers ONISEP détaillées'
    
    # IDEO référentiels
    elif 'ideo-formations_initiales' in name_lower:
        suggestions['config_key'] = 'formations_ideo'
        suggestions['output_dir'] = 'output/ideo_formations'
        suggestions['type'] = 'formations_ideo'
        suggestions['description'] = 'Référentiel formations IDEO'
    elif 'ideo-metiers_onisep' in name_lower:
        suggestions['config_key'] = 'metiers_ideo'
        suggestions['output_dir'] = 'output/ideo_metiers'
        suggestions['type'] = 'metiers_ideo'
        suggestions['description'] = 'Référentiel métiers IDEO'
    
    # Actions de formation
    elif 'actions_de_formation' in name_lower:
        if 'college' in name_lower:
            suggestions['config_key'] = 'actions_college'
            suggestions['output_dir'] = 'output/ideo_actions_college'
            suggestions['description'] = 'Actions formation collège'
        elif 'lycee' in name_lower:
            suggestions['config_key'] = 'actions_lycee'
            suggestions['output_dir'] = 'output/ideo_actions_lycee'
            suggestions['description'] = 'Actions formation lycée'
        elif 'superieur' in name_lower or 'enseignement_superieur' in name_lower:
            suggestions['config_key'] = 'actions_superieur'
            suggestions['output_dir'] = 'output/ideo_actions_superieur'
            suggestions['description'] = 'Actions formation supérieur'
    
    # Autres IDEO
    elif 'dispositif' in name_lower:
        suggestions['config_key'] = 'dispositifs'
        suggestions['output_dir'] = 'output/ideo_dispositifs'
        suggestions['description'] = 'Dispositifs'
    elif 'specialite' in name_lower:
        suggestions['config_key'] = 'specialites'
        suggestions['output_dir'] = 'output/ideo_specialites_premiere'
        suggestions['description'] = 'Spécialités première'
    elif 'optionnel' in name_lower:
        suggestions['config_key'] = 'optionnels'
        suggestions['output_dir'] = 'output/ideo_optionnels_seconde'
        suggestions['description'] = 'Optionnels seconde'
    elif 'langue' in name_lower:
        suggestions['config_key'] = 'langues'
        suggestions['output_dir'] = 'output/ideo_langues'
        suggestions['description'] = 'Langues au collège'
    elif 'structures' in name_lower:
        if 'secondaire' in name_lower:
            suggestions['config_key'] = 'structures_secondaire'
            suggestions['output_dir'] = 'output/ideo_structures_secondaire'
            suggestions['description'] = 'Structures secondaire'
        elif 'superieur' in name_lower:
            suggestions['config_key'] = 'structures_superieur'
            suggestions['output_dir'] = 'output/ideo_structures_superieur'
            suggestions['description'] = 'Structures supérieur'
    elif 'certification' in name_lower:
        suggestions['config_key'] = 'certifications'
        suggestions['output_dir'] = 'output/ideo_certifications'
        suggestions['description'] = 'Table certifications'
    
    # Fichier découpé ?
    if '_part' in name_lower:
        base_name = filename.rsplit('_part', 1)[0]
        suggestions['file_pattern'] = f"files/{base_name}_part*.xml"
        suggestions['notes'].append("⚠️  Fichier découpé détecté - Utiliser wildcard dans config")
        suggestions['notes'].append(f"   Pattern: {suggestions['file_pattern']}")
    else:
        suggestions['file_pattern'] = f"files/{filename}"
    
    # Suggestions basées sur la taille
    if size_mb > 50:
        suggestions['notes'].append(f"⚠️  Fichier > 50MB ({size_mb:.1f} MB)")
        suggestions['notes'].append("   → Lancer: python split_large_xml.py")
        suggestions['notes'].append("   → Puis utiliser wildcard: files/nom_part*.xml")
    elif size_mb > 40:
        suggestions['notes'].append(f"ℹ️  Fichier proche de 50MB ({size_mb:.1f} MB)")
        suggestions['notes'].append("   → Surveiller si mis à jour")
    
    # Suggestions basées sur le contenu
    if item_count == 0:
        suggestions['notes'].append("⚠️  Aucun item trouvé - Vérifier la structure XML")
    elif item_count > 10000:
        suggestions['notes'].append(f"ℹ️  Beaucoup d'items ({item_count:,})")
        suggestions['notes'].append("   → Conversion peut prendre du temps")
    
    # Si pas de config_key, générer un par défaut
    if not suggestions['config_key']:
        safe_name = filename.replace('.xml', '').replace('-', '_').replace('.', '_')
        suggestions['config_key'] = safe_name
        suggestions['output_dir'] = f"output/{safe_name}"
        suggestions['description'] = f"Fichier {filename}"
        suggestions['notes'].append("ℹ️  Configuration générée automatiquement")
        suggestions['notes'].append("   → Personnaliser si nécessaire")
    
    return suggestions


def generate_toml_config(suggestions):
    """Génère la configuration TOML pour un fichier."""
    lines = []
    lines.append(f"[conversions.{suggestions['config_key']}]")
    lines.append(f'file = "{suggestions["file_pattern"]}"')
    lines.append(f'output = "{suggestions["output_dir"]}"')
    lines.append(f'type = "{suggestions["type"]}"')
    lines.append(f'description = "{suggestions["description"]}"')
    
    return '\n'.join(lines)


# ============================================================================
# AFFICHAGE
# ============================================================================

def display_report(conn, scan_result):
    """Affiche le rapport complet."""
    cursor = conn.cursor()
    
    print("\n" + "═"*70)
    print("📊 DÉTECTION ET ANALYSE DES FICHIERS XML")
    print("═"*70)
    print()
    
    # Résumé du scan
    print("📁 Résumé du scan:")
    print(f"   Total fichiers: {scan_result['total']}")
    print(f"   Nouveaux: {len(scan_result['new'])}")
    print(f"   Modifiés: {len(scan_result['modified'])}")
    print(f"   Inchangés: {len(scan_result['unchanged'])}")
    print()
    
    # Nouveaux fichiers
    if scan_result['new']:
        print("═"*70)
        print("🆕 NOUVEAUX FICHIERS DÉTECTÉS")
        print("═"*70)
        print()
        
        for xml_file in scan_result['new']:
            suggestions = suggest_config_for_file(cursor, xml_file.name)
            
            print(f"📄 {xml_file.name}")
            print(f"   Taille: {suggestions['size_mb']:.1f} MB")
            print(f"   Items: {suggestions['item_count']:,}")
            print()
            
            if suggestions['notes']:
                print("   💡 Notes:")
                for note in suggestions['notes']:
                    print(f"   {note}")
                print()
            
            print("   📝 Configuration suggérée:")
            print()
            for line in generate_toml_config(suggestions).split('\n'):
                print(f"   {line}")
            print()
            print("   " + "-"*66)
            print()
    
    # Fichiers modifiés
    if scan_result['modified']:
        print("═"*70)
        print("🔄 FICHIERS MODIFIÉS")
        print("═"*70)
        print()
        
        for xml_file in scan_result['modified']:
            suggestions = suggest_config_for_file(cursor, xml_file.name)
            print(f"📄 {xml_file.name}")
            print(f"   Taille: {suggestions['size_mb']:.1f} MB")
            print(f"   Items: {suggestions['item_count']:,}")
            if suggestions['notes']:
                for note in suggestions['notes']:
                    print(f"   {note}")
            print()
    
    # Tous les fichiers configurés
    cursor.execute("""
        SELECT filename, filesize_mb, item_count, configured
        FROM xml_files
        ORDER BY filename
    """)
    
    print("═"*70)
    print("📋 TOUS LES FICHIERS TRACKÉS")
    print("═"*70)
    print()
    
    for row in cursor.fetchall():
        filename, size_mb, item_count, configured = row
        status = "✅" if configured else "⚠️ "
        print(f"{status} {filename:60} {size_mb:>6.1f} MB  {item_count:>7,} items")
    
    print()
    
    # Statistiques
    cursor.execute("SELECT COUNT(*) FROM xml_files WHERE configured = 0")
    unconfigured = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM xml_files")
    total = cursor.fetchone()[0]
    
    print("═"*70)
    print("📊 STATISTIQUES")
    print("═"*70)
    print(f"   Fichiers total: {total}")
    print(f"   Configurés: {total - unconfigured}")
    print(f"   À configurer: {unconfigured}")
    print()
    
    if unconfigured > 0:
        print("💡 Actions recommandées:")
        print("   1. Copier les configurations suggérées dans config.toml")
        print("   2. Personnaliser si nécessaire")
        print("   3. Lancer: ./convert_all.sh")
        print("   4. Marquer comme configuré: python detect_files.py --mark-configured")
    
    print()
    print("═"*70)


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Fonction principale."""
    import sys
    
    conn = init_database()
    
    # Options
    if '--mark-configured' in sys.argv:
        # Marquer tous les fichiers comme configurés
        cursor = conn.cursor()
        cursor.execute("UPDATE xml_files SET configured = 1")
        conn.commit()
        print("✅ Tous les fichiers marqués comme configurés")
        return
    
    if '--reset' in sys.argv:
        # Réinitialiser la base
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS xml_files")
        conn.commit()
        init_database()
        print("✅ Base de données réinitialisée")
    
    # Scanner et afficher le rapport
    scan_result = scan_files(conn)
    display_report(conn, scan_result)
    
    conn.close()


if __name__ == "__main__":
    main()
