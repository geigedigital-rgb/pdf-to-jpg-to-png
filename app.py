#!/usr/bin/env python3
"""
Flask web application for PDF to Image converter.
A clean, one-page interface for converting PDFs to image-based PDFs.
"""

import os
import tempfile
import shutil
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from pathlib import Path
import uuid
from pdf_to_image_converter import PDFToImageConverter
from utils import validate_pdf, format_file_size

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pdf-converter-secret-key-change-in-production'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page with the conversion interface."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and conversion."""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400
        
        # Get conversion settings
        dpi = int(request.form.get('dpi', 150))
        image_format = request.form.get('format', 'JPEG').upper()
        quality = int(request.form.get('quality', 85))
        
        # Validate settings
        if dpi not in [72, 150, 300]:
            return jsonify({'error': 'Invalid DPI value'}), 400
        if image_format not in ['JPEG', 'PNG']:
            return jsonify({'error': 'Invalid image format'}), 400
        if not 1 <= quality <= 100:
            return jsonify({'error': 'Invalid quality value'}), 400
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        secure_name = secure_filename(file.filename)
        input_filename = f"{file_id}_{secure_name}"
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
        
        # Save uploaded file
        file.save(input_path)
        
        # Validate PDF file
        if not validate_pdf(input_path):
            os.remove(input_path)
            return jsonify({'error': 'Invalid or corrupted PDF file'}), 400
        
        # Generate output filename
        base_name = Path(secure_name).stem
        output_filename = f"{file_id}_{base_name}_image_{dpi}dpi.pdf"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Convert PDF
        converter = PDFToImageConverter(
            dpi=dpi,
            image_format=image_format,
            jpeg_quality=quality,
            verbose=False
        )
        
        converter.convert_single_pdf(input_path, output_path)
        
        # Get file sizes
        input_size = os.path.getsize(input_path)
        output_size = os.path.getsize(output_path)
        
        # Clean up input file
        os.remove(input_path)
        
        return jsonify({
            'success': True,
            'file_id': file_id,
            'filename': output_filename,
            'original_size': format_file_size(input_size),
            'converted_size': format_file_size(output_size),
            'settings': {
                'dpi': dpi,
                'format': image_format,
                'quality': quality if image_format == 'JPEG' else None
            }
        })
        
    except Exception as e:
        # Clean up files on error
        if 'input_path' in locals() and os.path.exists(input_path):
            os.remove(input_path)
        if 'output_path' in locals() and os.path.exists(output_path):
            os.remove(output_path)
        
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500

@app.route('/download/<file_id>/<filename>')
def download_file(file_id, filename):
    """Download converted PDF file."""
    try:
        # Security: ensure filename contains the file_id to prevent unauthorized access
        if not filename.startswith(file_id):
            return jsonify({'error': 'Invalid file access'}), 403
        
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        # Get original filename for download
        parts = filename.split('_', 2)  # Split on first two underscores
        if len(parts) >= 3:
            original_base = parts[2].rsplit('_image_', 1)[0]  # Remove the _image_XXXdpi part
            download_name = f"{original_base}_converted.pdf"
        else:
            download_name = filename
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=download_name,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

@app.route('/cleanup/<file_id>/<filename>', methods=['POST'])
def cleanup_file(file_id, filename):
    """Clean up converted file after download."""
    try:
        if not filename.startswith(file_id):
            return jsonify({'error': 'Invalid file access'}), 403
        
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': f'Cleanup failed: {str(e)}'}), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    return jsonify({'error': 'File too large. Maximum size is 50MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Handle server errors."""
    return jsonify({'error': 'Internal server error'}), 500

# Background task to clean up old files
def cleanup_old_files():
    """Remove files older than 1 hour."""
    import time
    current_time = time.time()
    
    for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    file_age = current_time - os.path.getctime(file_path)
                    if file_age > 3600:  # 1 hour
                        try:
                            os.remove(file_path)
                        except OSError:
                            pass

if __name__ == '__main__':
    # Clean up old files on startup
    cleanup_old_files()
    
    # Run the app
    app.run(host='0.0.0.0', port=5000, debug=True)