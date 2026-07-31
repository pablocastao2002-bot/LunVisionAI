
import ollama

def generate_llm_report(
    result,
    confidence
):
    result = str(result).upper()

    # CASO NORMAL
    if result == "NORMAL":
        prompt_normal = f"""
Eres un radiólogo especializado en cáncer de pulmón.

Responde SIEMPRE en español.

NO escribas:
- Nombre del paciente
- Fecha del paciente
- Edad del paciente
- Sexo del paciente
- Campos vacíos
- Formularios

La respuesta debe contener EXCLUSIVAMENTE esta estructura:

Informe Médico

-Hallazgos:
No se han identificado hallazgos compatibles con cáncer pulmonar en el TAC analizado según la evaluación realizada por el modelo de inteligencia artificial.
-No existen signos sugestivos de cáncer pulmonar.

-Interpretación:
La clasificación automática obtenida corresponde a un estudio sin evidencia de signos sugestivos de cáncer pulmonar. No existe constancia de masas, tumores ni hallazgos sospechosos relacionados con cáncer pulmonar según el resultado proporcionado por el modelo.

-Recomendación:
Se recomienda mantener el seguimiento clínico habitual y consultar con un profesional sanitario ante la aparición de síntomas o factores de riesgo relevantes.

-Advertencia:
Este informe ha sido generado automáticamente mediante un modelo de inteligencia artificial como herramienta de apoyo al análisis radiológico. Los resultados presentados no constituyen un diagnóstico médico definitivo y deben ser interpretados y validados por profesionales sanitarios cualificados. La decisión clínica final debe basarse en la evaluación integral del paciente, su historia clínica, exploración clínica y las pruebas complementarias pertinentes.

"""

        response = ollama.chat(
            model="llama3",
            messages=[
                {
                    "role": "user",
                    "content": prompt_normal
                }
            ]
        )

        return response["message"]["content"]

    # CASO CÁNCER
    elif result != "NORMAL":
        prompt_abnormal = f"""
Eres un radiólogo especializado en cáncer de pulmón.

Responde SIEMPRE en español.

NO escribas:
- Nombre del paciente
- Fecha del paciente
- Edad del paciente
- Sexo del paciente
- Campos vacíos
- Formularios

La respuesta debe contener EXCLUSIVAMENTE esta estructura:

Informe Médico

-Hallazgos:
(texto)

-Interpretación:
(texto)

-Recomendación:
(texto)

-Advertencia:
Este informe ha sido generado automáticamente mediante un modelo de inteligencia artificial como herramienta de apoyo al análisis radiológico. Los resultados presentados no constituyen un diagnóstico médico definitivo y deben ser interpretados y validados por profesionales sanitarios cualificados. La decisión clínica final debe basarse en la evaluación integral del paciente, su historia clínica, exploración clínica y las pruebas complementarias pertinentes.

Resultado del modelo:
{result}

Confianza:
{confidence:.2f}%
"""

        response = ollama.chat(
            model="llama3",
            messages=[
                {
                    "role": "user",
                    "content": prompt_abnormal
                }
            ]
        )

        return response["message"]["content"]


