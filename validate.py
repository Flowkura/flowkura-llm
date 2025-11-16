#!/usr/bin/env python3
"""
Script de validation de la qualité des fichiers Markdown générés.
Vérifie que les fichiers sont bien formatés et ne contiennent pas d'erreurs.
"""

from pathlib import Path
import re


def validate_file(filepath):
    """Valide un fichier Markdown."""
    issues = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        # Vérifier qu'il y a un titre principal
        if not lines or not lines[0].startswith('# '):
            issues.append("Pas de titre principal (H1)")
        
        # Vérifier qu'il n'y a pas de balises HTML résiduelles
        html_tags = re.findall(r'<(?!h[1-6]>|/h[1-6]>|p>|/p>)[^>]+>', content)
        if html_tags:
            issues.append(f"Balises HTML détectées: {len(html_tags)}")
        
        # Vérifier qu'il n'y a pas de CDATA
        if 'CDATA' in content:
            issues.append("Sections CDATA non nettoyées")
        
        # Vérifier la longueur minimale
        if len(content) < 100:
            issues.append("Fichier trop court (< 100 caractères)")
        
        # Vérifier qu'il y a des sections
        h2_count = content.count('\n## ')
        if h2_count == 0:
            issues.append("Aucune section H2 trouvée")
        
        return len(issues) == 0, issues
        
    except Exception as e:
        return False, [f"Erreur de lecture: {str(e)}"]


def validate_directory(directory, sample_size=100):
    """Valide un échantillon de fichiers dans un dossier."""
    md_files = list(Path(directory).glob("*.md"))
    
    if not md_files:
        return None
    
    # Prendre un échantillon
    import random
    sample = random.sample(md_files, min(sample_size, len(md_files)))
    
    valid_count = 0
    invalid_files = []
    
    for filepath in sample:
        is_valid, issues = validate_file(filepath)
        if is_valid:
            valid_count += 1
        else:
            invalid_files.append({
                'file': filepath.name,
                'issues': issues
            })
    
    return {
        'total_checked': len(sample),
        'valid_count': valid_count,
        'invalid_count': len(invalid_files),
        'success_rate': (valid_count / len(sample) * 100) if sample else 0,
        'invalid_files': invalid_files[:10]  # Limiter à 10 exemples
    }


def main():
    """Fonction principale."""
    print("=" * 70)
    print("✅ VALIDATION DE LA QUALITÉ DES FICHIERS MARKDOWN")
    print("=" * 70)
    print()
    
    # Valider les formations
    print("📚 FORMATIONS")
    print("-" * 70)
    formations_results = validate_directory("output/formations", sample_size=100)
    
    if formations_results:
        print(f"  Fichiers vérifiés  : {formations_results['total_checked']}")
        print(f"  Fichiers valides   : {formations_results['valid_count']}")
        print(f"  Fichiers invalides : {formations_results['invalid_count']}")
        print(f"  Taux de succès     : {formations_results['success_rate']:.1f}%")
        
        if formations_results['invalid_files']:
            print("\n  ⚠️  Exemples de fichiers avec problèmes:")
            for item in formations_results['invalid_files'][:5]:
                print(f"     - {item['file']}")
                for issue in item['issues']:
                    print(f"       → {issue}")
    else:
        print("  ❌ Aucun fichier trouvé")
    
    print()
    
    # Valider les métiers
    print("💼 MÉTIERS")
    print("-" * 70)
    metiers_results = validate_directory("output/metiers", sample_size=100)
    
    if metiers_results:
        print(f"  Fichiers vérifiés  : {metiers_results['total_checked']}")
        print(f"  Fichiers valides   : {metiers_results['valid_count']}")
        print(f"  Fichiers invalides : {metiers_results['invalid_count']}")
        print(f"  Taux de succès     : {metiers_results['success_rate']:.1f}%")
        
        if metiers_results['invalid_files']:
            print("\n  ⚠️  Exemples de fichiers avec problèmes:")
            for item in metiers_results['invalid_files'][:5]:
                print(f"     - {item['file']}")
                for issue in item['issues']:
                    print(f"       → {issue}")
    else:
        print("  ❌ Aucun fichier trouvé")
    
    print()
    
    # Résumé global
    if formations_results and metiers_results:
        total_checked = formations_results['total_checked'] + metiers_results['total_checked']
        total_valid = formations_results['valid_count'] + metiers_results['valid_count']
        total_invalid = formations_results['invalid_count'] + metiers_results['invalid_count']
        global_rate = (total_valid / total_checked * 100) if total_checked else 0
        
        print("🌍 RÉSUMÉ GLOBAL")
        print("-" * 70)
        print(f"  Total vérifié      : {total_checked} fichiers")
        print(f"  Total valide       : {total_valid} fichiers")
        print(f"  Total invalide     : {total_invalid} fichiers")
        print(f"  Taux de succès     : {global_rate:.1f}%")
        print()
        
        if global_rate >= 95:
            print("  ✅ Excellente qualité de conversion!")
        elif global_rate >= 80:
            print("  ✓  Bonne qualité de conversion")
        else:
            print("  ⚠️  Des améliorations sont nécessaires")
    
    print()
    print("=" * 70)
    print("✅ Validation terminée")
    print("=" * 70)


if __name__ == "__main__":
    main()
