from fpdf import FPDF

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

def generate_pdf(requirements, output_path):
    pdf = PDF()
    pdf.add_page()

    for paragraph, classification in requirements:
        pdf.chapter_title('Requisito:')
        pdf.chapter_body(paragraph)
        pdf.chapter_title('ClasificaciÃ³n:')
        pdf.chapter_body(classification)

    pdf.output(output_path)