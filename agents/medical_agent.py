
import ollama


def generate_report(prediction, confidence):

    prompt = f"""
    Eres un especialista en radiología pulmonar.

    Resultado del modelo de IA:

    Clase: {prediction}

    Confianza: {confidence:.2f}%

    Explica al paciente:

    - Qué significa el resultado
    - Qué implica
    - Recomendaciones generales

    No hagas diagnósticos definitivos.
    No afirmes que existe cáncer con certeza.
    Responde en español.
    """

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]

