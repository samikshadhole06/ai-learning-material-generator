from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfgen import canvas
from io import BytesIO
import re


def markdown_to_pdf(markdown_text, filename="notes.pdf"):
    """
    Convert markdown notes to a professional PDF document.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
    )
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles for elegant formatting
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#000000',
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='#000000',
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#333333',
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        textColor='#000000',
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )
    
    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Code'],
        fontSize=9,
        textColor='#000000',
        fontName='Courier',
        leftIndent=20,
        spaceAfter=8
    )
    
    # Build document content
    story = []
    
    # Split markdown into lines
    lines = markdown_text.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if not line:
            story.append(Spacer(1, 0.1*inch))
            continue
        
        # Handle headings
        if line.startswith('# '):
            text = line[2:].strip()
            story.append(Paragraph(text, title_style))
        elif line.startswith('## '):
            text = line[3:].strip()
            story.append(Paragraph(text, heading1_style))
        elif line.startswith('### '):
            text = line[4:].strip()
            story.append(Paragraph(text, heading2_style))
        
        # Handle bullet points
        elif line.startswith('- ') or line.startswith('• '):
            text = '• ' + line[2:].strip()
            story.append(Paragraph(text, body_style))
        
        # Handle numbered lists
        elif re.match(r'^\d+\.', line):
            story.append(Paragraph(line, body_style))
        
        # Handle bold text
        elif '**' in line:
            line = line.replace('**', '<b>').replace('**', '</b>')
            story.append(Paragraph(line, body_style))
        
        # Regular paragraphs
        else:
            story.append(Paragraph(line, body_style))
    
    # Build PDF
    doc.build(story)
    
    # Get PDF data
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data
