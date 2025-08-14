#!/usr/bin/env python3
"""
Create a test PDF file for demonstrating the PDF to image converter.
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle

def create_test_pdf(filename="test_document.pdf"):
    """Create a test PDF with text, graphics, and vector elements."""
    
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Page 1: Text and simple graphics
    c.setTitle("Test PDF Document")
    
    # Header
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(width/2, height - 50, "Test PDF Document")
    
    # Subtitle
    c.setFont("Helvetica", 14)
    c.setFillColor(colors.black)
    c.drawCentredString(width/2, height - 80, "This PDF contains vector graphics, text, and shapes")
    
    # Rectangle with gradient effect
    c.setFillColor(colors.lightblue)
    c.rect(50, height - 200, 200, 80, fill=1, stroke=1)
    
    # Circle
    c.setFillColor(colors.red)
    c.circle(350, height - 150, 30, fill=1, stroke=1)
    
    # Text content
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    
    text_lines = [
        "This is a test PDF document created to demonstrate",
        "the PDF to image converter functionality.",
        "",
        "The converter will rasterize all vector elements,",
        "text, and graphics into images while maintaining",
        "the original page dimensions and layout.",
        "",
        "Features demonstrated:",
        "• Vector graphics (rectangles, circles)",
        "• Different fonts and text sizes", 
        "• Color fills and strokes",
        "• Multiple pages with different content"
    ]
    
    y_position = height - 250
    for line in text_lines:
        c.drawString(50, y_position, line)
        y_position -= 20
    
    # Add some vector lines
    c.setStrokeColor(colors.green)
    c.setLineWidth(3)
    c.line(50, 100, width - 50, 100)
    
    c.showPage()
    
    # Page 2: More complex graphics
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.purple)
    c.drawCentredString(width/2, height - 50, "Page 2: Complex Graphics")
    
    # Create a table-like structure with rectangles
    colors_list = [colors.red, colors.green, colors.blue, colors.yellow, colors.orange]
    
    for i, color in enumerate(colors_list):
        x = 50 + i * 100
        y = height - 200
        c.setFillColor(color)
        c.rect(x, y, 80, 50, fill=1, stroke=1)
        
        # Add text on top of rectangles
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(x + 40, y + 25, f"Box {i+1}")
    
    # Create some paths and curves
    c.setStrokeColor(colors.black)
    c.setLineWidth(2)
    
    # Bezier curve
    path = c.beginPath()
    path.moveTo(50, height - 300)
    path.curveTo(150, height - 250, 250, height - 350, 350, height - 300)
    path.curveTo(450, height - 250, 550, height - 350, width - 50, height - 300)
    c.drawPath(path)
    
    # Text explaining the conversion
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.black)
    
    explanation = [
        "After conversion to image-based PDF:",
        "• All vector elements become rasterized pixels",
        "• Text becomes non-selectable image data", 
        "• File size may be reduced significantly",
        "• Visual quality depends on chosen DPI setting",
        "",
        "This is useful for:",
        "• Flattening complex documents",
        "• Reducing file size",
        "• Converting vector graphics to images",
        "• Ensuring consistent appearance across platforms"
    ]
    
    y_pos = height - 450
    for line in explanation:
        c.drawString(50, y_pos, line)
        y_pos -= 18
    
    # Save the PDF
    c.save()
    print(f"Test PDF created: {filename}")

if __name__ == "__main__":
    create_test_pdf()