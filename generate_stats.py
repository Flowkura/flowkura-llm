#!/usr/bin/env python3
"""
Script pour générer des statistiques sur les fichiers Markdown générés.
"""

from pathlib import Path
import os


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
    
    # Analyser les formations
    formations_dir = "output/formations"
    formations_stats = analyze_directory(formations_dir)
    
    if formations_stats:
        print("📚 FORMATIONS")
        print("-" * 60)
        print(f"  Nombre de fichiers     : {formations_stats['total_files']:,}")
        print(f"  Taille totale          : {format_size(formations_stats['total_size'])}")
        print(f"  Taille moyenne/fichier : {format_size(formations_stats['avg_size'])}")
        print(f"  Taille min             : {format_size(formations_stats['min_size'])}")
        print(f"  Taille max             : {format_size(formations_stats['max_size'])}")
        print(f"  Nombre total de lignes : {formations_stats['total_lines']:,}")
        print(f"  Moyenne lignes/fichier : {formations_stats['avg_lines']:.1f}")
        print()
    else:
        print(f"❌ Aucun fichier trouvé dans {formations_dir}")
        print()
    
    # Analyser les métiers
    metiers_dir = "output/metiers"
    metiers_stats = analyze_directory(metiers_dir)
    
    if metiers_stats:
        print("💼 MÉTIERS")
        print("-" * 60)
        print(f"  Nombre de fichiers     : {metiers_stats['total_files']:,}")
        print(f"  Taille totale          : {format_size(metiers_stats['total_size'])}")
        print(f"  Taille moyenne/fichier : {format_size(metiers_stats['avg_size'])}")
        print(f"  Taille min             : {format_size(metiers_stats['min_size'])}")
        print(f"  Taille max             : {format_size(metiers_stats['max_size'])}")
        print(f"  Nombre total de lignes : {metiers_stats['total_lines']:,}")
        print(f"  Moyenne lignes/fichier : {metiers_stats['avg_lines']:.1f}")
        print()
    else:
        print(f"❌ Aucun fichier trouvé dans {metiers_dir}")
        print()
    
    # Statistiques globales
    if formations_stats and metiers_stats:
        print("🌍 TOTAL GLOBAL")
        print("-" * 60)
        total_files = formations_stats['total_files'] + metiers_stats['total_files']
        total_size = formations_stats['total_size'] + metiers_stats['total_size']
        total_lines = formations_stats['total_lines'] + metiers_stats['total_lines']
        
        print(f"  Nombre total de fichiers : {total_files:,}")
        print(f"  Taille totale            : {format_size(total_size)}")
        print(f"  Nombre total de lignes   : {total_lines:,}")
        print()
        
        # Ratios
        print("📈 RATIOS")
        print("-" * 60)
        formations_pct = (formations_stats['total_files'] / total_files * 100)
        metiers_pct = (metiers_stats['total_files'] / total_files * 100)
        print(f"  Formations : {formations_pct:.1f}% des fichiers")
        print(f"  Métiers    : {metiers_pct:.1f}% des fichiers")
        print()
    
    print("=" * 60)
    print("✅ Analyse terminée")
    print("=" * 60)


if __name__ == "__main__":
    main()
