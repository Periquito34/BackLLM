from fpdf import FPDF
import os
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Requisitos Clasificados', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

def generate_pdf(requirements):
    # Directorio donde se guardarán los archivos
    output_dir = 'generated_files'

    # Crear directorio si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generar un nombre único para el archivo PDF usando la fecha y hora actual
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"processed_requirements_{timestamp}.pdf"
    output_path = os.path.join(output_dir, output_filename)

    pdf = PDF()
    pdf.add_page()

    for paragraph, classification in requirements:
        pdf.chapter_title('Requisito:')
        pdf.chapter_body(paragraph)
        pdf.chapter_title('Clasificación:')
        pdf.chapter_body(str(classification))  # Convertir a cadena de texto antes de pasarlo

    pdf.output(output_path)
    return output_path
