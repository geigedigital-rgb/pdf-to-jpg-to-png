#!/usr/bin/env python3
"""
Generate requirements.txt for the PDF to Image Converter project.
This script creates a requirements file based on the current environment.
"""

import subprocess
import sys
from pathlib import Path

def get_package_version(package_name):
    """Get the version of an installed package."""
    try:
        result = subprocess.run(
            [sys.executable, '-c', f'import {package_name}; print({package_name}.__version__)'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except:
        # Try alternative methods
        try:
            import pkg_resources
            return pkg_resources.get_distribution(package_name).version
        except:
            return None

def main():
    """Generate requirements.txt file."""
    
    # Core packages required for this project
    core_packages = {
        'Flask': 'flask',
        'PyMuPDF': 'fitz',
        'Pillow': 'PIL',
        'reportlab': 'reportlab',
        'psutil': 'psutil'
    }
    
    print("Generating requirements.txt for PDF to Image Converter...")
    print("=" * 60)
    
    requirements = []
    missing_packages = []
    
    for display_name, import_name in core_packages.items():
        version = get_package_version(import_name)
        if version:
            if display_name == 'PyMuPDF':
                # PyMuPDF is installed as PyMuPDF but imported as fitz
                requirements.append(f"PyMuPDF=={version}")
            elif display_name == 'Pillow':
                # Pillow is installed as Pillow but imported as PIL
                requirements.append(f"Pillow=={version}")
            else:
                requirements.append(f"{display_name}=={version}")
            print(f"✓ {display_name}: {version}")
        else:
            missing_packages.append(display_name)
            print(f"✗ {display_name}: Not found")
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install missing packages with:")
        print(f"pip install {' '.join(missing_packages)}")
        return
    
    # Write requirements file
    requirements_content = """# PDF to Image Converter - Requirements
# Generated automatically - edit with care

# Core dependencies
""" + '\n'.join(requirements) + """

# Python version requirement
# Requires Python 3.8 or higher
"""
    
    output_file = Path("requirements-generated.txt")
    with open(output_file, 'w') as f:
        f.write(requirements_content)
    
    print(f"\n✓ Requirements file generated: {output_file}")
    print("\nTo install these requirements in a new environment:")
    print(f"pip install -r {output_file}")
    
    # Also create a minimal version
    minimal_content = "# Minimal requirements - core packages only\n" + '\n'.join(requirements)
    minimal_file = Path("requirements-core.txt")
    with open(minimal_file, 'w') as f:
        f.write(minimal_content)
    
    print(f"✓ Minimal requirements file: {minimal_file}")

if __name__ == "__main__":
    main()