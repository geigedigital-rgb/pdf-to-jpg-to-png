#!/usr/bin/env python3
"""
PDF to Image-based PDF Converter

A command-line tool that converts PDFs to image-based PDFs with configurable
rasterization settings. Each page is converted to a rasterized image and
embedded in a new PDF while maintaining original dimensions.
"""

import argparse
import io
import os
import sys
from pathlib import Path
import tempfile
import shutil
from typing import List, Tuple, Optional

try:
    import fitz  # PyMuPDF
    from PIL import Image, ImageEnhance
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.utils import ImageReader
except ImportError as e:
    print(f"Error: Required library not found: {e}")
    print("Please install required packages:")
    print("pip install PyMuPDF Pillow reportlab")
    sys.exit(1)

from utils import validate_pdf, get_output_filename, format_file_size


class PDFToImageConverter:
    """Main converter class for PDF to image-based PDF conversion."""
    
    def __init__(self, dpi: int = 150, image_format: str = 'JPEG', 
                 jpeg_quality: int = 85, verbose: bool = False):
        """
        Initialize the converter with specified settings.
        
        Args:
            dpi: Resolution for rasterization (72, 150, 300)
            image_format: Output image format ('JPEG' or 'PNG')
            jpeg_quality: JPEG compression quality (1-100)
            verbose: Enable verbose output
        """
        self.dpi = dpi
        self.image_format = image_format.upper()
        self.jpeg_quality = jpeg_quality
        self.verbose = verbose
        
        # Validate settings
        if self.dpi not in [72, 150, 300]:
            raise ValueError("DPI must be 72, 150, or 300")
        if self.image_format not in ['JPEG', 'PNG']:
            raise ValueError("Image format must be JPEG or PNG")
        if not 1 <= self.jpeg_quality <= 100:
            raise ValueError("JPEG quality must be between 1 and 100")
    
    def log(self, message: str) -> None:
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(message)
    
    def convert_pdf_to_images(self, pdf_path: str, temp_dir: str) -> List[Tuple[str, Tuple[float, float]]]:
        """
        Convert PDF pages to images and save them to temporary directory.
        
        Args:
            pdf_path: Path to input PDF file
            temp_dir: Temporary directory for image files
            
        Returns:
            List of tuples containing (image_path, (width, height))
        """
        self.log(f"Opening PDF: {pdf_path}")
        
        try:
            pdf_document = fitz.open(pdf_path)
        except Exception as e:
            raise RuntimeError(f"Failed to open PDF: {e}")
        
        if pdf_document.is_encrypted:
            raise RuntimeError("PDF is password protected")
        
        page_count = len(pdf_document)
        self.log(f"Processing {page_count} pages at {self.dpi} DPI")
        
        image_paths = []
        
        for page_num in range(page_count):
            try:
                # Get page and create transformation matrix for desired DPI
                page = pdf_document[page_num]
                mat = fitz.Matrix(self.dpi / 72, self.dpi / 72)
                
                # Render page to pixmap
                pixmap = page.get_pixmap(matrix=mat, alpha=False)
                
                # Convert to PIL Image
                # Save pixmap to temporary file and load with PIL (more reliable method)
                temp_pixmap_path = os.path.join(temp_dir, f"temp_page_{page_num}.ppm")
                pixmap.save(temp_pixmap_path)
                pil_image = Image.open(temp_pixmap_path)
                os.remove(temp_pixmap_path)
                
                # Get original page dimensions in points
                page_rect = page.rect
                original_width = page_rect.width
                original_height = page_rect.height
                
                # Save image with appropriate format and quality
                image_filename = f"page_{page_num:04d}.{self.image_format.lower()}"
                image_path = os.path.join(temp_dir, image_filename)
                
                if self.image_format == 'JPEG':
                    # Convert to RGB if necessary (JPEG doesn't support transparency)
                    if pil_image.mode in ('RGBA', 'LA', 'P'):
                        rgb_image = Image.new('RGB', pil_image.size, (255, 255, 255))
                        if pil_image.mode == 'P':
                            pil_image = pil_image.convert('RGBA')
                        rgb_image.paste(pil_image, mask=pil_image.split()[-1] if pil_image.mode == 'RGBA' else None)
                        pil_image = rgb_image
                    
                    pil_image.save(image_path, 'JPEG', quality=self.jpeg_quality, optimize=True)
                else:  # PNG
                    pil_image.save(image_path, 'PNG', optimize=True)
                
                image_paths.append((image_path, (original_width, original_height)))
                
                self.log(f"Processed page {page_num + 1}/{page_count}")
                
                # Clean up
                pixmap = None
                pil_image.close()
                
            except Exception as e:
                raise RuntimeError(f"Failed to process page {page_num + 1}: {e}")
        
        pdf_document.close()
        return image_paths
    
    def create_pdf_from_images(self, image_paths: List[Tuple[str, Tuple[float, float]]], 
                              output_path: str) -> None:
        """
        Create a new PDF from the rasterized images.
        
        Args:
            image_paths: List of (image_path, (width, height)) tuples
            output_path: Path for output PDF file
        """
        self.log(f"Creating output PDF: {output_path}")
        
        try:
            # Create PDF canvas
            c = canvas.Canvas(output_path)
            
            for i, (image_path, (width, height)) in enumerate(image_paths):
                self.log(f"Adding page {i + 1}/{len(image_paths)} to PDF")
                
                # Set page size to match original dimensions
                c.setPageSize((width, height))
                
                # Create ImageReader object
                img_reader = ImageReader(image_path)
                
                # Draw image to fill entire page
                c.drawImage(img_reader, 0, 0, width=width, height=height)
                
                # Finish the page
                c.showPage()
            
            # Save the PDF
            c.save()
            self.log("PDF creation completed")
            
        except Exception as e:
            raise RuntimeError(f"Failed to create output PDF: {e}")
    
    def convert_single_pdf(self, input_path: str, output_path: Optional[str] = None) -> str:
        """
        Convert a single PDF file to image-based PDF.
        
        Args:
            input_path: Path to input PDF file
            output_path: Optional path for output file
            
        Returns:
            Path to the created output file
        """
        # Validate input file
        if not validate_pdf(input_path):
            raise ValueError(f"Invalid PDF file: {input_path}")
        
        # Generate output filename if not provided
        if output_path is None:
            output_path = get_output_filename(input_path, self.image_format.lower(), self.dpi)
        
        # Create temporary directory for images
        with tempfile.TemporaryDirectory() as temp_dir:
            self.log(f"Using temporary directory: {temp_dir}")
            
            try:
                # Convert PDF pages to images
                image_paths = self.convert_pdf_to_images(input_path, temp_dir)
                
                # Create new PDF from images
                self.create_pdf_from_images(image_paths, output_path)
                
                # Get file sizes for reporting
                input_size = os.path.getsize(input_path)
                output_size = os.path.getsize(output_path)
                
                print(f"Conversion completed:")
                print(f"  Input:  {input_path} ({format_file_size(input_size)})")
                print(f"  Output: {output_path} ({format_file_size(output_size)})")
                print(f"  Pages:  {len(image_paths)}")
                print(f"  Format: {self.image_format} at {self.dpi} DPI")
                
                if self.image_format == 'JPEG':
                    print(f"  Quality: {self.jpeg_quality}%")
                
                return output_path
                
            except Exception as e:
                # Clean up output file if it was created but conversion failed
                if os.path.exists(output_path):
                    os.remove(output_path)
                raise e
    
    def convert_batch(self, input_paths: List[str], output_dir: Optional[str] = None) -> List[str]:
        """
        Convert multiple PDF files in batch mode.
        
        Args:
            input_paths: List of input PDF file paths
            output_dir: Optional output directory
            
        Returns:
            List of created output file paths
        """
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        output_paths = []
        successful = 0
        failed = 0
        
        print(f"Starting batch conversion of {len(input_paths)} files...")
        
        for i, input_path in enumerate(input_paths, 1):
            print(f"\n[{i}/{len(input_paths)}] Processing: {os.path.basename(input_path)}")
            
            try:
                # Generate output path
                if output_dir:
                    base_name = os.path.splitext(os.path.basename(input_path))[0]
                    output_filename = f"{base_name}_image_{self.dpi}dpi.pdf"
                    output_path = os.path.join(output_dir, output_filename)
                else:
                    output_path = None
                
                # Convert the PDF
                result_path = self.convert_single_pdf(input_path, output_path)
                output_paths.append(result_path)
                successful += 1
                
            except Exception as e:
                print(f"ERROR: Failed to convert {input_path}: {e}")
                failed += 1
        
        print(f"\nBatch conversion completed:")
        print(f"  Successful: {successful}")
        print(f"  Failed: {failed}")
        print(f"  Total: {len(input_paths)}")
        
        return output_paths


def main():
    """Main entry point for the command-line interface."""
    parser = argparse.ArgumentParser(
        description="Convert PDFs to image-based PDFs with configurable rasterization settings",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.pdf
  %(prog)s input.pdf -o output.pdf --dpi 300 --format PNG
  %(prog)s *.pdf --batch --output-dir ./converted/
  %(prog)s file1.pdf file2.pdf --batch --dpi 150 --quality 90
        """
    )
    
    # Input arguments
    parser.add_argument('input', nargs='+', help='Input PDF file(s)')
    
    # Output arguments
    parser.add_argument('-o', '--output', help='Output file path (single file mode only)')
    parser.add_argument('--output-dir', help='Output directory (batch mode)')
    parser.add_argument('--batch', action='store_true', 
                       help='Enable batch mode for multiple files')
    
    # Conversion settings
    parser.add_argument('--dpi', type=int, choices=[72, 150, 300], default=150,
                       help='Rasterization DPI (default: 150)')
    parser.add_argument('--format', choices=['JPEG', 'PNG'], default='JPEG',
                       help='Image format (default: JPEG)')
    parser.add_argument('--quality', type=int, metavar='1-100', default=85,
                       help='JPEG quality percentage (default: 85)')
    
    # Other options
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--version', action='version', version='PDF to Image Converter 1.0')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not 1 <= args.quality <= 100:
        parser.error("JPEG quality must be between 1 and 100")
    
    if len(args.input) > 1 and not args.batch:
        parser.error("Multiple input files require --batch mode")
    
    if args.batch and args.output:
        parser.error("Cannot specify --output in batch mode, use --output-dir instead")
    
    # Validate input files
    for input_path in args.input:
        if not os.path.exists(input_path):
            parser.error(f"Input file not found: {input_path}")
        if not validate_pdf(input_path):
            parser.error(f"Invalid PDF file: {input_path}")
    
    try:
        # Create converter instance
        converter = PDFToImageConverter(
            dpi=args.dpi,
            image_format=args.format,
            jpeg_quality=args.quality,
            verbose=args.verbose
        )
        
        if args.batch or len(args.input) > 1:
            # Batch mode
            converter.convert_batch(args.input, args.output_dir)
        else:
            # Single file mode
            converter.convert_single_pdf(args.input[0], args.output)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
