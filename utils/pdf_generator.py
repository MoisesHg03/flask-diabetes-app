from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def generate_pdf(registro):
    """Genera un archivo PDF con los datos de un registro."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Encabezado
    elements.append(Paragraph("MINISTERIO DE SALUD PÚBLICA Y BIENESTAR SOCIAL - COLOMBIA", styles['Title']))
    elements.append(Paragraph("PREDICCIÓN DE DIABETES", styles['Heading2']))
    elements.append(Spacer(1, 12))

    # Tabla con datos
    data = [
        ["Campo", "Valor"],
        ["ID", str(registro[0])],
        ["Glucosa", f"{registro[1]} mg/dl"],
        ["Presión Arterial", f"{registro[2]} mmHg"],
        ["Grosor de Piel", f"{registro[3]} mm"],
        ["Insulina", f"{registro[4]} μU/ml"],
        ["IMC", f"{registro[5]} kg/m²"],
        ["Pedigrí Diabetes", f"{registro[6]}"],
        ["Edad", f"{registro[7]} años"],
        ["Embarazos", str(registro[8])],
        ["Resultado", registro[9]],
        ["Fecha", registro[10]]
    ]
    table = Table(data, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
    ]))
    elements.append(table)

    # Pie de página
    elements.append(Spacer(1, 24))
    elements.append(Paragraph("TU NOMBRE / MARCA - Diagnóstico Personalizado", styles['Normal']))

    # Generar PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer