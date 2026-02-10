#!/usr/bin/env python3
"""
Script pour extraire le pourcentage de couverture des tests depuis coverage.xml
et générer un fichier JSON pour les badges dynamiques.
"""
import xml.etree.ElementTree as ET
import json
import sys
import os


def extract_coverage_percentage(xml_file: str = "coverage.xml") -> float:
    """Extrait le pourcentage de couverture depuis le fichier coverage.xml."""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Le format coverage.xml a une structure comme:
        # <coverage line-rate="0.79" branch-rate="0.68" ...>
        line_rate = float(root.get("line-rate", "0"))
        return round(line_rate * 100, 2)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {xml_file}: {e}", file=sys.stderr)
        return 0.0


def generate_coverage_json(coverage_percentage: float, output_file: str = "coverage.json"):
    """Génère un fichier JSON avec les métriques de couverture."""
    data = {
        "schemaVersion": 1,
        "label": "coverage",
        "message": f"{coverage_percentage:.1f}%",
        "color": "brightgreen" if coverage_percentage >= 70 else "yellow" if coverage_percentage >= 50 else "red",
        "cacheSeconds": 3600
    }
    
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Fichier {output_file} généré avec couverture: {coverage_percentage:.1f}%")


def main():
    """Fonction principale."""
    xml_file = sys.argv[1] if len(sys.argv) > 1 else "coverage.xml"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "coverage.json"
    
    if not os.path.exists(xml_file):
        print(f"Erreur: Le fichier {xml_file} n'existe pas.", file=sys.stderr)
        sys.exit(1)
    
    coverage_percentage = extract_coverage_percentage(xml_file)
    generate_coverage_json(coverage_percentage, output_file)
    
    # Affiche également le pourcentage pour le workflow GitHub Actions
    print(f"::set-output name=coverage_percentage::{coverage_percentage:.1f}")
    print(f"::set-output name=coverage_color::{'brightgreen' if coverage_percentage >= 70 else 'yellow' if coverage_percentage >= 50 else 'red'}")


if __name__ == "__main__":
    main()