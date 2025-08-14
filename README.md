# PDF to Image Converter

A Python application that converts PDFs to image-based PDFs with configurable rasterization settings. Available both as a command-line tool and a clean web interface. Each page of the input PDF is converted to a rasterized image and embedded in a new PDF while maintaining the original page dimensions and aspect ratios.

## Features

- **Two Interfaces**: Clean web interface and powerful command-line tool
- **Configurable DPI**: Support for 72, 150, and 300 DPI rasterization
- **Multiple Image Formats**: Choose between JPEG and PNG for rasterization
- **Quality Control**: Adjustable JPEG compression quality (1-100%)
- **Batch Processing**: Convert multiple PDFs in a single operation (CLI)
- **Original Dimensions**: Maintains original page sizes and aspect ratios
- **Memory Efficient**: Handles large PDFs with optimized memory usage
- **Progress Tracking**: Visual progress indication for large files
- **Error Handling**: Robust error handling for corrupted or protected PDFs
- **Drag & Drop**: Easy file upload in web interface

## Web Interface

Start the web application:

```bash
python app.py
```

Then open your browser to `http://localhost:5000`. The web interface provides:

- **Clean Design**: One-page interface with intuitive controls
- **Drag & Drop**: Simply drag PDF files into the upload zone
- **Live Settings**: Adjust DPI, format, and quality in real-time
- **Progress Tracking**: Visual progress bar during conversion
- **Instant Download**: Download converted files immediately

## Installation & Deployment

### Quick Setup
```bash
# Install dependencies
pip install -r requirements-minimal.txt

# Run the web application
python app.py
```

### Deployment Options

**Auto-generated requirements** (recommended):
```bash
python generate_requirements.py
pip install -r requirements-generated.txt
```

**Pre-configured requirements**:
- `requirements-minimal.txt` - Core packages only
- `requirements-deployment.txt` - Complete with all dependencies

See `DEPLOYMENT.md` for detailed deployment instructions including Docker, production servers, and troubleshooting.

## Command-Line Tool

For advanced users and batch processing:

```bash
# Basic usage after installing requirements
