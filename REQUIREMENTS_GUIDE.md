# Requirements Files Guide

This project provides multiple requirements files to suit different deployment scenarios.

## Available Requirements Files

### 1. `requirements-minimal.txt` ⭐ **RECOMMENDED**
**Best for most deployments**
- Contains only core packages
- Allows pip to resolve compatible sub-dependencies automatically
- Smallest file, fastest installation
- Most flexible for different environments

```bash
pip install -r requirements-minimal.txt
```

**Contents:**
```
Flask==3.1.1
PyMuPDF==1.26.3
Pillow==11.3.0
reportlab==4.4.3
psutil==7.0.0
```

### 2. `requirements-deployment.txt`
**For production environments requiring exact versions**
- Includes all sub-dependencies with exact versions
- Ensures 100% reproducible builds
- Larger file, longer installation time
- More rigid, may conflict with other packages

```bash
pip install -r requirements-deployment.txt
```

### 3. `requirements-generated.txt`
**Auto-generated from current environment**
- Created by running `python generate_requirements.py`
- Reflects current working versions
- Good for capturing a working state

```bash
python generate_requirements.py
pip install -r requirements-generated.txt
```

### 4. `requirements-core.txt`
**Alternative minimal version**
- Generated automatically by the requirements script
- Same as minimal but created dynamically

## Which File Should You Use?

### For Local Development
```bash
pip install -r requirements-minimal.txt
```

### For Production Deployment
```bash
pip install -r requirements-minimal.txt
```

### For Docker/Container Deployment
```bash
pip install -r requirements-minimal.txt
```

### For CI/CD Pipelines
```bash
pip install -r requirements-deployment.txt
```

### For Troubleshooting
```bash
python generate_requirements.py
# Then use the generated file
```

## Installation Commands

### Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements-minimal.txt
```

### System-wide Installation
```bash
pip install -r requirements-minimal.txt
```

### Upgrade Existing Installation
```bash
pip install -r requirements-minimal.txt --upgrade
```

## Verification

After installation, verify all packages are working:

```bash
python -c "
import flask
import fitz  # PyMuPDF
import PIL  # Pillow
import reportlab
import psutil
print('✓ All packages imported successfully')
"
```

## Troubleshooting

### Common Issues

**Package conflicts:**
```bash
pip install -r requirements-minimal.txt --force-reinstall
```

**Outdated pip:**
```bash
pip install --upgrade pip
pip install -r requirements-minimal.txt
```

**Permission errors:**
```bash
pip install -r requirements-minimal.txt --user
```

### Platform-Specific Notes

**Windows:**
- All packages have pre-built wheels
- No compilation required

**macOS:**
- May need Xcode command line tools for some packages
- `xcode-select --install`

**Linux:**
- May need development headers
- `apt-get install python3-dev` (Ubuntu/Debian)
- `yum install python3-devel` (RHEL/CentOS)

## Package Versions

The pinned versions in these files are tested and known to work together:

- **Flask 3.1.1**: Web framework with security updates
- **PyMuPDF 1.26.3**: Latest stable PDF processing
- **Pillow 11.3.0**: Current stable image processing
- **ReportLab 4.4.3**: PDF generation with latest features
- **psutil 7.0.0**: System monitoring capabilities

These versions are compatible with Python 3.8 through 3.12.