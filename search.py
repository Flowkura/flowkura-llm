#!/usr/bin/env python3
"""
Script de recherche dans les fichiers Markdown générés.
Permet de trouver rapidement des formations ou métiers par mots-clés.
"""

import sys
from pathlib import Path
import re


def search_in_files(directory, keyword, max_results=10):
    """Recherche un mot-clé dans les fichiers d'un dossier."""
    md_files = list(Path(directory).glob("*.md"))
    results = []
    
    keyword_lower = keyword.lower()
    
    for filepath in md_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Chercher dans le nom du fichier
                if keyword_lower in filepath.name.lower():
                    # Extraire le titre (première ligne)
                    first_line = content.split('\n')[0].strip('# ')
                    results.append({
                        'file': filepath.name,
                        'title': first_line,
                        'match_type': 'filename',
                        'context': ''
                    })
                # Chercher dans le contenu
                elif keyword_lower in content.lower():
                    first_line = content.split('\n')[0].strip('# ')
                    
                    # Trouver le contexte
                    lines = content.split('\n')
                    context_lines = []
                    for i, line in enumerate(lines):
                        if keyword_lower in line.lower():
                            start = max(0, i - 1)
                            end = min(len(lines), i + 2)
                            context_lines = lines[start:end]
                            break
                    
                    context = '\n'.join(context_lines)
                    
                    results.append({
                        'file': filepath.name,
                        'title': first_line,
                        'match_type': 'content',
                        'context': context[:200]  # Limiter le contexte
                    })
                    
            if len(results) >= max_results:
                break
                
        except Exception as e:
            continue
    
    return results


def main():
    """Fonction principale."""
    if len(sys.argv) < 2:
        print("Usage: python search.py <mot-clé> [max_results]")
        print("")
        print("Exemples:")
        print("  python search.py informatique")
        print("  python search.py 'intelligence artificielle' 20")
        print("  python search.py développeur")
        sys.exit(1)
    
    keyword = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    print(f"🔍 Recherche de '{keyword}'...")
    print("=" * 70)
    print()
    
    # Rechercher dans les formations
    print("📚 FORMATIONS")
    print("-" * 70)
    formations_results = search_in_files("output/formations", keyword, max_results)
    
    if formations_results:
        for i, result in enumerate(formations_results, 1):
            print(f"\n{i}. {result['title']}")
            print(f"   📄 Fichier: {result['file']}")
            if result['context']:
                print(f"   📝 Contexte: {result['context'][:100]}...")
    else:
        print("   Aucun résultat trouvé")
    
    print()
    print()
    
    # Rechercher dans les métiers
    print("💼 MÉTIERS")
    print("-" * 70)
    metiers_results = search_in_files("output/metiers", keyword, max_results)
    
    if metiers_results:
        for i, result in enumerate(metiers_results, 1):
            print(f"\n{i}. {result['title']}")
            print(f"   📄 Fichier: {result['file']}")
            if result['context']:
                print(f"   📝 Contexte: {result['context'][:100]}...")
    else:
        print("   Aucun résultat trouvé")
    
    print()
    print("=" * 70)
    total_results = len(formations_results) + len(metiers_results)
    print(f"✅ {total_results} résultat(s) trouvé(s)")
    print()


if __name__ == "__main__":
    main()
