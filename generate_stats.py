#!/usr/bin/env python3
"""
Script pour générer des statistiques sur les fichiers Markdown générés.
"""

from pathlib import Path
import os
import tomllib


def analyze_directory(directory):
    """Analyse un dossier de fichiers Markdown."""
    md_files = list(Path(directory).glob("*.md"))
    
    if not md_files:
        return None
    
    total_files = len(md_files)
    total_size = sum(f.stat().st_size for f in md_files)
    avg_size = total_size / total_files if total_files > 0 else 0
    
    sizes = [f.stat().st_size for f in md_files]
    min_size = min(sizes)
    max_size = max(sizes)
    
    # Compter les lignes
    total_lines = 0
    for f in md_files:
        with open(f, 'r', encoding='utf-8') as file:
            total_lines += sum(1 for _ in file)
    
    avg_lines = total_lines / total_files if total_files > 0 else 0
    
    return {
        'total_files': total_files,
        'total_size': total_size,
        'avg_size': avg_size,
        'min_size': min_size,
        'max_size': max_size,
        'total_lines': total_lines,
        'avg_lines': avg_lines
    }


def format_size(size_bytes):
    """Formate la taille en octets de manière lisible."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def main():
    """Fonction principale."""
    print("=" * 60)
    print("📊 STATISTIQUES DES FICHIERS MARKDOWN GÉNÉRÉS")
    print("=" * 60)
    print()
    
    # Charger la configuration
    config_file = Path("config.toml")
    if not config_file.exists():
        print("❌ Fichier config.toml introuvable")
        return
    
    with open(config_file, "rb") as f:
        config = tomllib.load(f)
    
    if "conversions" not in config:
        print("❌ Aucune conversion définie dans config.toml")
        return
    
    all_stats = []
    
    # Analyser chaque conversion définie dans le config
    for name, conv_config in config["conversions"].items():
        output_dir = conv_config.get("output")
        description = conv_config.get("description", name)
        
        if not output_dir:
            continue
        
        stats = analyze_directory(output_dir)
        
        if stats:
            stats['name'] = name
            stats['description'] = description
            stats['output_dir'] = output_dir
            all_stats.append(stats)
            
            print(f"📁 {description.upper()}")
            print("-" * 60)
            print(f"  Dossier                : {output_dir}")
            print(f"  Nombre de fichiers     : {stats['total_files']:,}")
            print(f"  Taille totale          : {format_size(stats['total_size'])}")
            print(f"  Taille moyenne/fichier : {format_size(stats['avg_size'])}")
            print(f"  Taille min             : {format_size(stats['min_size'])}")
            print(f"  Taille max             : {format_size(stats['max_size'])}")
            print(f"  Nombre total de lignes : {stats['total_lines']:,}")
            print(f"  Moyenne lignes/fichier : {stats['avg_lines']:.1f}")
            print()
        else:
            print(f"⚠️  {description.upper()}")
            print("-" * 60)
            print(f"  Dossier : {output_dir}")
            print(f"  ❌ Aucun fichier trouvé")
            print()
    
    # Statistiques globales
    if all_stats:
        print("🌍 TOTAL GLOBAL")
        print("-" * 60)
        total_files = sum(s['total_files'] for s in all_stats)
        total_size = sum(s['total_size'] for s in all_stats)
        total_lines = sum(s['total_lines'] for s in all_stats)
        
        print(f"  Nombre total de fichiers : {total_files:,}")
        print(f"  Taille totale            : {format_size(total_size)}")
        print(f"  Nombre total de lignes   : {total_lines:,}")
        print()
        
        # Ratios par type
        print("📈 RÉPARTITION PAR TYPE")
        print("-" * 60)
        for stats in sorted(all_stats, key=lambda x: x['total_files'], reverse=True):
            pct = (stats['total_files'] / total_files * 100)
            print(f"  {stats['description']:30} : {stats['total_files']:6,} fichiers ({pct:5.1f}%)")
        print()
    else:
        print("❌ Aucun fichier Markdown trouvé dans les dossiers de sortie")
        print()
    
    print("=" * 60)
    print("✅ Analyse terminée")
    print("=" * 60)


if __name__ == "__main__":
    main()
