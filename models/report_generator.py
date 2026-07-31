
def generate_report(
    result,
    confidence
):

    if result == "CANCER":

        findings = (
            "El modelo de Deep Learning detecta "
            "patrones compatibles con cáncer pulmonar."
        )

        interpretation = (
            "El resultado indica una alta probabilidad "
            "de presencia de anomalías pulmonares."
        )

        recommendation = (
            "Se recomienda evaluación médica "
            "especializada para confirmar el diagnóstico."
        )

    else:

        findings = (
            "No se detectan patrones compatibles "
            "con cáncer pulmonar."
        )

        interpretation = (
            "La radiografía presenta características "
            "compatibles con tejido pulmonar normal."
        )

        recommendation = (
            "Mantener controles médicos rutinarios."
        )

    report = f"""
INFORME AUTOMÁTICO

Hallazgos:
{findings}

Nivel de confianza:
{confidence:.2f}%

Interpretación:
{interpretation}

Recomendación:
{recommendation}
"""

    return report
