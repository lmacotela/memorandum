"""Servicio para generar documentos Word desde plantillas."""
import os
import uuid
from docx import Document

TEMPLATES_DIR = "templates"
OUTPUT_DIR = "output"


def _replace_in_paragraph(paragraph, replacements: dict[str, str]):
    full_text = "".join(run.text for run in paragraph.runs)
    if not any(key in full_text for key in replacements):
        return
    new_text = full_text
    for placeholder, value in replacements.items():
        new_text = new_text.replace(placeholder, str(value))
    if paragraph.runs:
        paragraph.runs[0].text = new_text
        for run in paragraph.runs[1:]:
            run.text = ""


def _replace_in_document(doc: Document, replacements: dict[str, str]):
    for paragraph in doc.paragraphs:
        _replace_in_paragraph(paragraph, replacements)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    _replace_in_paragraph(paragraph, replacements)


def generar_documento(registro: dict, titulo: str, template_name: str = "memorandum.docx") -> str:
    """
    Genera un .docx desde un registro del API de Sapiens.
    Retorna la ruta al archivo generado.
    """
    template_path = os.path.join(TEMPLATES_DIR, template_name)
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Plantilla no encontrada: {template_path}")

    # Mapeo de campos del API a placeholders del template
    # Ajusta los nombres de campo según la respuesta real del API
    replacements = {
        "<NombreEmpleado>": registro.get("nombreEmpleado") or registro.get("NombreEmpleado") or registro.get("nombre") or "",
        "<Asunto>":         registro.get("asunto")         or registro.get("Asunto")         or "",
        "<fecha>":          registro.get("fecha")          or registro.get("Fecha")          or registro.get("fechaInicio") or "",
        "<días>":           str(registro.get("dias")       or registro.get("Dias")           or registro.get("cantidadDias") or ""),
        "<Documento>":      registro.get("documento")      or registro.get("Documento")      or registro.get("nroDocumento") or "",
    }

    doc = Document(template_path)
    doc.core_properties.title = titulo
    _replace_in_document(doc, replacements)

    output_filename = f"{uuid.uuid4().hex}.docx"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    doc.save(output_path)

    return output_path
