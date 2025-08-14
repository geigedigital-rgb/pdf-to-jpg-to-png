"""
Utility functions for the PDF to Image converter.
"""

import os
import mimetypes
from pathlib import Path
from typing import Optional


def validate_pdf(file_path: str) -> bool:
    """
    Validate if a file is a valid PDF.
    
    Args:
        file_path: Path to the file to validate
        
    Returns:
        True if file appears to be a valid PDF, False otherwise
    """
    if not os.path.exists(file_path):
        return False
    
    if not os.path.isfile(file_path):
        return False
    
    # Check file extension
    if not file_path.lower().endswith('.pdf'):
        return False
    
    # Check MIME type
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type != 'application/pdf':
        # Try reading the file header as fallback
        try:
            with open(file_path, 'rb') as f:
                header = f.read(5)
                if not header.startswith(b'%PDF-'):
                    return False
        except (IOError, OSError):
            return False
    
    # Check minimum file size (empty PDFs are usually at least a few hundred bytes)
    try:
        if os.path.getsize(file_path) < 100:
            return False
    except (IOError, OSError):
        return False
    
    return True


def get_output_filename(input_path: str, image_format: str, dpi: int) -> str:
    """
    Generate an appropriate output filename based on input path and settings.
    
    Args:
        input_path: Path to the input PDF file
        image_format: Image format being used ('jpeg' or 'png')
        dpi: DPI setting being used
        
    Returns:
        Generated output filename
    """
    input_path_obj = Path(input_path)
    
    # Extract base name without extension
    base_name = input_path_obj.stem
    
    # Create descriptive suffix
    suffix = f"_image_{dpi}dpi"
    
    # Construct output filename
    output_name = f"{base_name}{suffix}.pdf"
    
    # Use same directory as input file
    output_path = input_path_obj.parent / output_name
    
    # Handle filename conflicts by adding a number
    counter = 1
    original_output_path = output_path
    
    while output_path.exists():
        name_with_counter = f"{base_name}{suffix}_{counter}.pdf"
        output_path = input_path_obj.parent / name_with_counter
        counter += 1
        
        # Prevent infinite loop
        if counter > 1000:
            break
    
    return str(output_path)


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: File size in bytes
        
    Returns:
        Formatted file size string
    """
    if size_bytes == 0:
        return "0 B"
    
    # Define size units
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0
    size = float(size_bytes)
    
    # Convert to appropriate unit
    while size >= 1024.0 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1
    
    # Format with appropriate precision
    if unit_index == 0:  # Bytes
        return f"{int(size)} {units[unit_index]}"
    else:
        return f"{size:.1f} {units[unit_index]}"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing or replacing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename safe for filesystem use
    """
    # Characters that are problematic in filenames
    invalid_chars = '<>:"/\\|?*'
    
    # Replace invalid characters with underscores
    sanitized = filename
    for char in invalid_chars:
        sanitized = sanitized.replace(char, '_')
    
    # Remove leading/trailing whitespace and dots
    sanitized = sanitized.strip(' .')
    
    # Ensure filename is not empty
    if not sanitized:
        sanitized = "converted_pdf"
    
    # Limit length to reasonable size (most filesystems support 255 chars)
    if len(sanitized) > 200:
        sanitized = sanitized[:200]
    
    return sanitized


def expand_glob_patterns(patterns: list) -> list:
    """
    Expand glob patterns in file paths to actual file paths.
    
    Args:
        patterns: List of file paths that may contain glob patterns
        
    Returns:
        List of expanded file paths
    """
    import glob
    
    expanded_paths = []
    
    for pattern in patterns:
        # If pattern contains glob characters, expand it
        if any(char in pattern for char in ['*', '?', '[', ']']):
            matches = glob.glob(pattern)
            if matches:
                expanded_paths.extend(sorted(matches))
            else:
                # No matches found for pattern
                print(f"Warning: No files found matching pattern: {pattern}")
        else:
            # Regular file path
            expanded_paths.append(pattern)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_paths = []
    for path in expanded_paths:
        if path not in seen:
            seen.add(path)
            unique_paths.append(path)
    
    return unique_paths


def create_directory_if_not_exists(directory_path: str) -> bool:
    """
    Create directory if it doesn't exist.
    
    Args:
        directory_path: Path to the directory to create
        
    Returns:
        True if directory exists or was created successfully, False otherwise
    """
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path, exist_ok=True)
        return True
    except (OSError, IOError) as e:
        print(f"Error creating directory {directory_path}: {e}")
        return False


def get_available_memory() -> Optional[int]:
    """
    Get available system memory in bytes.
    
    Returns:
        Available memory in bytes, or None if unable to determine
    """
    try:
        import psutil
        return psutil.virtual_memory().available
    except ImportError:
        # psutil not available, try to estimate from /proc/meminfo on Linux
        try:
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if line.startswith('MemAvailable:'):
                        # Extract memory in KB and convert to bytes
                        mem_kb = int(line.split()[1])
                        return mem_kb * 1024
        except (FileNotFoundError, ValueError, IOError):
            pass
    
    return None


def estimate_memory_usage(pdf_page_count: int, dpi: int, image_format: str) -> int:
    """
    Estimate memory usage for PDF conversion.
    
    Args:
        pdf_page_count: Number of pages in the PDF
        dpi: DPI setting for rasterization
        image_format: Image format ('JPEG' or 'PNG')
        
    Returns:
        Estimated memory usage in bytes
    """
    # Rough estimate based on typical page sizes and image data
    # Assuming average page size of 8.5" x 11" (US Letter)
    
    width_inches = 8.5
    height_inches = 11.0
    
    # Calculate pixel dimensions
    width_pixels = int(width_inches * dpi)
    height_pixels = int(height_inches * dpi)
    
    # Calculate bytes per pixel (RGB = 3 bytes, RGBA = 4 bytes)
    bytes_per_pixel = 3 if image_format.upper() == 'JPEG' else 4
    
    # Calculate memory per page
    bytes_per_page = width_pixels * height_pixels * bytes_per_pixel
    
    # Add overhead for PDF processing and temporary storage
    overhead_multiplier = 2.5
    
    total_memory = int(pdf_page_count * bytes_per_page * overhead_multiplier)
    
    return total_memory
