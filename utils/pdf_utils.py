from io import BytesIO
from uuid import uuid4

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import CSS, HTML


def render_pdf(template_src, context_dict=None, css_styles=None):
    """
    Render a beautifully styled PDF with a dark background and colorful text.

    :param template_src: Path to the Django template.
    :param context_dict: context_dict dictionary for rendering the template.
    :param css_styles: Optional string containing additional custom CSS.
    :return: Bytes of the generated PDF.
    """
    context_dict = context_dict or {}

    html_string = render_to_string(template_src, context_dict)
    html = HTML(string=html_string, base_url=settings.BASE_DIR)

    # Default dark theme CSS with vibrant text colors
    default_css = CSS(
        string="""
        @page {
            size: A4;
            margin: 20mm;
            background-color: #000000;
        }
        body {
            font-family: 'Arial', sans-serif;
            color: rgb(200, 200, 200);
            background-color: #000000;
            line-height: 1.8;
            font-size: 13pt;
        }
        header, footer {
            text-align: center;
            font-size: 10pt;
            color: rgb(150, 150, 150);
        }
        h1, h2, h3 {
            color: rgb(255, 100, 100);  /* Vibrant red for headers */
            text-align: center;
            margin-bottom: 18px;
        }
        p {
            color: rgb(180, 180, 250);  /* Soft bluish text for paragraphs */
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 25px;
            background-color: #1a1a1a;
        }
        table th, table td {
            border: 1px solid rgb(70, 70, 70);
            padding: 12px;
            text-align: center;
            color: rgb(220, 220, 220);
        }
        table th {
            background-color: rgb(50, 50, 50);
            color: rgb(255, 180, 80);  /* Warm yellow for table headers */
        }
        table tr:nth-child(even) {
            background-color: rgb(30, 30, 30);
        }
        table tr:nth-child(odd) {
            background-color: rgb(45, 45, 45);
        }
    """
    )

    styles = [default_css]
    if css_styles:
        styles.append(CSS(string=css_styles))

    pdf_io = BytesIO()
    html.write_pdf(target=pdf_io, stylesheets=styles)

    return pdf_io.getvalue()


def pdf_response(pdf_content, filename=None):
    """
    Generate an HTTP response with the generated PDF content.

    :param pdf_content: PDF content in bytes.
    :param filename: Optional name of the downloaded PDF file. Generates a unique filename if not provided.
    :return: HttpResponse with the PDF file attached.
    """
    unique_filename = filename or f"document_{uuid4().hex}.pdf"
    response = HttpResponse(pdf_content, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{unique_filename}"'
    return response
