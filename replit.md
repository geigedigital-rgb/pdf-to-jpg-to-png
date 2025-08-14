# PDF to Image Converter

## Overview

This is a Python application that converts PDFs to image-based PDFs with configurable rasterization settings. The application is available in two forms: a clean web interface for easy single-file conversions and a powerful command-line tool for batch processing. It takes PDF files as input, converts each page to a rasterized image, and embeds these images into a new PDF while maintaining original page dimensions and aspect ratios. It supports multiple DPI settings (72, 150, 300), different image formats (JPEG, PNG), and adjustable compression quality.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Components

**Web Application (`app.py`)**
- Flask-based web interface for single-file PDF conversions
- Clean, modern UI with drag-and-drop file upload
- Real-time settings adjustment and visual progress tracking
- Secure file handling with automatic cleanup
- RESTful API endpoints for upload, conversion, and download

**Main Converter Class (`PDFToImageConverter`)**
- Handles the primary conversion logic from PDF to image-based PDF
- Configurable settings for DPI, image format, JPEG quality, and verbosity
- Designed as a class-based architecture for reusability and state management
- Used by both web interface and command-line tool

**Utility Module (`utils.py`)**
- Contains helper functions for PDF validation and file operations
- Implements robust PDF file validation using multiple checks (file extension, MIME type, file header, minimum size)
- Provides file utility functions for output filename generation and file size formatting

**Command-Line Interface**
- Built using Python's `argparse` module for parameter handling
- Supports batch processing of multiple PDF files
- Configurable output settings and progress tracking

### Processing Pipeline

**Input Validation**
- Multi-layer PDF validation: file existence, extension check, MIME type verification, and file header inspection
- Minimum file size validation to catch empty or corrupted files

**Conversion Process**
- Page-by-page rasterization using PyMuPDF for PDF reading
- Image processing with PIL (Pillow) for format conversion and quality adjustment
- PDF generation using ReportLab to embed rasterized images while preserving original dimensions

**Memory Management**
- Designed for memory-efficient handling of large PDF files
- Uses temporary files and cleanup processes to manage memory usage during conversion

### Error Handling

**Robust Error Management**
- Comprehensive error handling for corrupted or protected PDFs
- Graceful handling of missing dependencies with clear installation instructions
- File validation prevents processing of invalid inputs

## External Dependencies

### Core Libraries

**PyMuPDF (fitz)**
- Primary PDF reading and page rendering library
- Handles PDF parsing and page-to-image conversion
- Provides high-quality rasterization capabilities

**Pillow (PIL)**
- Image processing and format conversion
- Handles JPEG/PNG format selection and quality adjustments
- Provides image enhancement capabilities

**ReportLab**
- PDF generation library for creating output PDFs
- Embeds rasterized images while maintaining page dimensions
- Handles canvas creation and page layout

### Standard Library Dependencies

**Built-in Modules**
- `argparse` for command-line interface
- `pathlib` and `os` for file system operations
- `tempfile` for temporary file management
- `mimetypes` for file type validation
- `shutil` for file operations

### System Requirements

**Python Environment**
- Requires Python 3.x
- Cross-platform compatibility (Windows, macOS, Linux)
- Command-line execution environment

**File System**
- Read access to input PDF files
- Write access to output directory
- Temporary storage space for intermediate processing