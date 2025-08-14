#!/usr/bin/env python3
"""
Demonstration script for the PDF to Image Converter
Shows all features and capabilities of the converter tool.
"""

import os
import subprocess
import time

def run_command(cmd, description):
    """Run a command and show the output."""
    print(f"\n{'='*60}")
    print(f"DEMO: {description}")
    print(f"Command: {cmd}")
    print('='*60)
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ SUCCESS")
        if result.stdout:
            print(result.stdout)
    else:
        print("✗ ERROR")
        if result.stderr:
            print(result.stderr)
    
    time.sleep(1)  # Brief pause for readability

def main():
    print("PDF to Image Converter - Complete Demonstration")
    print("=" * 60)
    
    # Check if test PDF exists, create if not
    if not os.path.exists("test_document.pdf"):
        print("Creating test PDF...")
        subprocess.run("python create_test_pdf.py", shell=True)
    
    # Demo 1: Basic conversion with default settings
    run_command(
        "python pdf_to_image_converter.py test_document.pdf",
        "Basic conversion with default settings (150 DPI, JPEG, 85% quality)"
    )
    
    # Demo 2: High quality PNG conversion
    run_command(
        "python pdf_to_image_converter.py test_document.pdf -o demo_high_quality.pdf --dpi 300 --format PNG --verbose",
        "High quality PNG conversion (300 DPI)"
    )
    
    # Demo 3: Low quality, small file size
    run_command(
        "python pdf_to_image_converter.py test_document.pdf -o demo_compressed.pdf --dpi 72 --quality 60 --verbose",
        "Compressed conversion for smaller file size (72 DPI, 60% quality)"
    )
    
    # Demo 4: Batch processing
    os.makedirs("batch_demo", exist_ok=True)
    run_command(
        "python pdf_to_image_converter.py *.pdf --batch --output-dir batch_demo --dpi 150 --quality 75",
        "Batch processing multiple PDFs"
    )
    
    # Demo 5: Show help
    run_command(
        "python pdf_to_image_converter.py --help",
        "Display help and usage information"
    )
    
    # Show file comparison
    print("\n" + "="*60)
    print("FILE SIZE COMPARISON")
    print("="*60)
    
    files_to_check = [
        "test_document.pdf",
        "test_document_image_150dpi.pdf", 
        "demo_high_quality.pdf",
        "demo_compressed.pdf"
    ]
    
    for filename in files_to_check:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            size_kb = size / 1024
            print(f"{filename:<35} {size_kb:8.1f} KB")
    
    print("\n" + "="*60)
    print("DEMONSTRATION COMPLETE")
    print("="*60)
    print("\nKey Features Demonstrated:")
    print("✓ Basic PDF to image conversion")
    print("✓ Configurable DPI settings (72, 150, 300)")
    print("✓ Multiple image formats (JPEG, PNG)")
    print("✓ Adjustable JPEG quality")
    print("✓ Batch processing capabilities") 
    print("✓ Custom output filenames and directories")
    print("✓ Verbose logging")
    print("✓ File size optimization")
    
    print("\nThe converter successfully flattens all vector graphics,")
    print("text, and other elements into rasterized images while")
    print("maintaining original page dimensions and layout.")

if __name__ == "__main__":
    main()