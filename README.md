# 🫁 LungVisionAI

> **Plataforma para la detección de cáncer pulmonar mediante Inteligencia Artificial a partir de TACs torácicos**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![PyTorch](https://img.shields.io/badge/Framework-PyTorch-EE4C2C?logo=pytorch)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit)
![License](https://img.shields.io/badge/Licencia-MIT-green)

---

## 📋 Descripción del Proyecto

**LungVisionAI** es un sistema inteligente diseñado para asistir a profesionales de la salud en la clasificación de tomografías axiales computarizadas (TAC) de tórax. 
La aplicación utiliza modelos de redes neuronales profundas para:
- Analizar automáticamente TACs torácicos.
- Detectar o Rechazar la presencia de anomalías cancerígenas en más de un 95% de probabilidad.
- Explica visualmente a través de mapas de calor Grad-CAM los cuales muestran que región es la afectada influyendo así en la predicción y aportando transparencia al modelo.
- Por último se generan informes médicos automáticos en formato PDF reduciendo así tiempos de documentación.

---

## 🔬 Características Principales

* **Clasificación Automática de TAC:** Clasificación binaria rápida con porcentaje de confianza (*ej. CÁNCER - Confianza: 99.81%*).
* **Explicabilidad Visual (Grad-CAM):** Generación de mapas de calor para resaltar las regiones de interés en las que el modelo enfoca su predicción.
* **Informes Médicos Automatizados:** Generación automática de informes en PDF con hallazgos, interpretación radiológica, recomendaciones y advertencias legales.

---

## 📊 Muestra de Resultados y Reportes

La aplicación genera reportes médicos completos que incluyen los mapas de activación visual y el análisis del modelo:

| Análisis TAC | Mapa de Calor (Grad-CAM) | Superposición |
| :---: | :---: | :---: |
| **TAC Torácico Original** | **Áreas de Atención del Modelo** | **Superposición sobre TAC** |

<details>
<summary>🔍 <b>Ejemplo de Informe Médico Generado por la App</b></summary>

* **Resultado:** CÁNCER (Confianza: 99.81%)
* **Hallazgos:** Presencia de nódulos o tumores neoplásicos con análisis de densidad y lesiones asociadas.
* **Interpretación:** Correlación diagnóstica basada en patrones detectados en la tomografía.
* **Recomendación:** Sugerencias clínicas de abordaje y seguimiento especializado.
* **Descargo de responsabilidad:** Herramienta de apoyo al diagnóstico que debe ser validada por personal sanitario cualificado.

</details>

---

## 🚀 Instalación y Ejecución Local

### Requisitos

* Python 3.9 o superior
* En torno de desarrollo (Windows / Linux / macOS)

### Pasos

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/pablocastao2002-bot/LunVisionAI.git](https://github.com/pablocastao2002-bot/LunVisionAI.git)
   cd LunVisionAI
