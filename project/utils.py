import pdfplumber


def read_pdf(name):
    with pdfplumber.open(name) as pdf:
        return pdf.pages[0].extract_text()
