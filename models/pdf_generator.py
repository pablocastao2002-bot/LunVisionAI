
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from datetime import datetime

import os


def create_pdf(
    result,
    confidence,
    report,
    original_image_path,
    heatmap_path,
    overlay_path
):

    os.makedirs(
        "outputs",
        exist_ok=True
    )

    filename = (
        "outputs/lungvision_report.pdf"
    )

    doc = SimpleDocTemplate(
        filename
    )

    styles = getSampleStyleSheet()

    elements = []

    # --------------------------
    # PORTADA
    # --------------------------

    elements.append(
        Paragraph(
            "LungVisionAI Report",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(
            1,
            20
        )
    )

    elements.append(
        Paragraph(
            f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            styles["Normal"]
        )
    )

    elements.append(
        Spacer(
            1,
            10
        )
    )

    elements.append(
        Paragraph(
            f"Resultado: {result}",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            f"Confianza: {confidence:.2f}%",
            styles["Heading2"]
        )
    )

    elements.append(
        Spacer(
            1,
            20
        )
    )

    # --------------------------
    # TAC ORIGINAL
    # --------------------------

    elements.append(
        Paragraph(
            "TAC Analizado",
            styles["Heading1"]
        )
    )

    elements.append(
        Spacer(
            1,
            10
        )
    )

    if os.path.exists(
        original_image_path
    ):
        elements.append(
            Image(
                original_image_path,
                width=300,
                height=300
            )
        )

    elements.append(
        Spacer(
            1,
            20
        )
    )

    # --------------------------
    # HEATMAP
    # --------------------------

    elements.append(
        Paragraph(
            "Grad-CAM",
            styles["Heading1"]
        )
    )

    elements.append(
        Spacer(
            1,
            10
        )
    )

    if os.path.exists(
        heatmap_path
    ):
        elements.append(
            Paragraph(
                "Mapa de Calor",
                styles["Heading2"]
            )
        )

        elements.append(
            Image(
                heatmap_path,
                width=250,
                height=250
            )
        )

    elements.append(
        Spacer(
            1,
            15
        )
    )

    if os.path.exists(
        overlay_path
    ):
        elements.append(
            Paragraph(
                "Superposición sobre el TAC",
                styles["Heading2"]
            )
        )

        elements.append(
            Image(
                overlay_path,
                width=250,
                height=250
            )
        )

    # --------------------------
    # NUEVA PÁGINA
    # --------------------------

    elements.append(
        PageBreak()
    )

    elements.append(
        Paragraph(
            "Informe Médico",
            styles["Heading1"]
        )
    )

    elements.append(
        Spacer(
            1,
            15
        )
    )

    # --------------------------
    # LIMPIEZA DEL TEXTO
    # --------------------------

    if report is None:
        report = ""

    report = str(report).strip()

    report = report.replace(
        "Nombre del paciente:",
        ""
    )

    report = report.replace(
        "Patient Name:",
        ""
    )

    report = report.replace(
        "Insert patient name",
        ""
    )

    report = report.replace(
        "Insert date",
        ""
    )

    report = report.replace(
        "Date:",
        ""
    )

    # --------------------------
    # SI OLLAMA FALLA
    # --------------------------

    if report == "":

        report = """
Hallazgos:
No disponibles.

Interpretación:
No disponible.

Recomendación:
Se recomienda valoración médica especializada.

Advertencia:
Este informe ha sido generado automáticamente mediante inteligencia artificial y no sustituye la evaluación realizada por profesionales sanitarios cualificados.
"""

    # --------------------------
    # MOSTRAR INFORME COMPLETO
    # --------------------------

    report = report.replace(
        "\n",
        "<br/>"
    )

    elements.append(
        Paragraph(
            report,
            styles["BodyText"]
        )
    )

    doc.build(
        elements
    )

    return filename

