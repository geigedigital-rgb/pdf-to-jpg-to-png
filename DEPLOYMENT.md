# Deployment Guide

This guide covers deploying the PDF to Image Converter outside of Replit.

## Quick Start

1. **Clone or download the project files**
2. **Install dependencies**:
   ```bash
   pip install -r requirements-minimal.txt
   ```
3. **Run the web application**:
   ```bash
   python app.py
   ```
4. **Access the application** at `http://localhost:5000`

## System Requirements

- **Python**: 3.8 or higher (3.11+ recommended)
- **Memory**: Minimum 512MB RAM (2GB+ recommended for large PDFs)
- **Storage**: Space for temporary files during conversion
- **Operating System**: Windows, macOS, or Linux

## Dependencies

### Core Packages
- `Flask==3.1.1` - Web framework
- `PyMuPDF==1.26.3` - PDF processing
- `Pillow==11.3.0` - Image manipulation
- `reportlab==4.4.3` - PDF generation
- `psutil==7.0.0` - System monitoring

### Installation Options

**Option 1: Minimal (Recommended)**
```bash
pip install -r requirements-minimal.txt
```

**Option 2: Complete with all sub-dependencies**
```bash
pip install -r requirements-deployment.txt
```

**Option 3: Manual installation**
```bash
pip install Flask PyMuPDF Pillow reportlab psutil
```

## Production Deployment

### Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements-minimal.txt
```

### Configuration
Create a production configuration by modifying `app.py`:

```python
# Change for production
app.config['SECRET_KEY'] = 'your-secure-random-secret-key'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB

# Run with production server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

### Production WSGI Server
For production, use a proper WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements-minimal.txt .
RUN pip install -r requirements-minimal.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t pdf-converter .
docker run -p 5000:5000 pdf-converter
```

## File Structure

```
pdf-converter/
├── app.py                      # Flask web application
├── pdf_to_image_converter.py   # Core converter class
├── utils.py                    # Utility functions
├── templates/
│   └── index.html             # Web interface
├── requirements-minimal.txt    # Core dependencies
├── requirements-deployment.txt # Complete dependencies
├── uploads/                   # Temporary upload directory
├── outputs/                   # Temporary output directory
└── DEPLOYMENT.md              # This file
```

## Security Considerations

1. **File Upload Limits**: Configure appropriate file size limits
2. **Input Validation**: PDF validation is built-in
3. **Temporary Files**: Automatic cleanup after 1 hour
4. **Secret Key**: Use a secure secret key in production
5. **File Access**: UUID-based file naming prevents unauthorized access

## Troubleshooting

### Common Issues

**ImportError: No module named 'fitz'**
```bash
pip install PyMuPDF
```

**Memory errors with large PDFs**
- Increase system memory
- Reduce DPI settings
- Process files in smaller batches

**Permission errors**
- Ensure write permissions for `uploads/` and `outputs/` directories
- Create directories if they don't exist:
```bash
mkdir -p uploads outputs
```

### Performance Optimization

1. **Memory**: Monitor with `psutil` integration
2. **Storage**: Regular cleanup of temporary files
3. **Processing**: Lower DPI for faster conversion
4. **Concurrent**: Use multiple worker processes for high traffic

## Command Line Tool

The command-line interface is also available for server deployments:

```bash
# Single file conversion
python pdf_to_image_converter.py input.pdf

# Batch processing
python pdf_to_image_converter.py *.pdf --batch --output-dir converted/

# Custom settings
python pdf_to_image_converter.py input.pdf --dpi 300 --format PNG
```

## Support

- Check logs for detailed error messages
- Ensure all dependencies are correctly installed
- Verify Python version compatibility (3.8+)
- Test with small PDF files first