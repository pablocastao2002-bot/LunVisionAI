
import os
import base64
import streamlit as st
from PIL import Image

from models.predict import predict
from models.lung_detector import is_lung_xray
from models.gradcam import generate_gradcam
from models.ollama_report import generate_llm_report
from models.pdf_generator import create_pdf


os.makedirs(
    "outputs",
    exist_ok=True
)


st.set_page_config(
    page_title="LungVision🫁AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>

#MainMenu {
    visibility:hidden;
}

footer {
    visibility:hidden;
}

header {
    visibility:hidden;
}

.block-container{
    max-width:1200px;
    padding-top:1rem;
}

.logo-container{
    text-align:center;
    margin-top:20px;
    margin-bottom:10px;
}

.logo-container img{
    width:650px;
}

.main-title{
    text-align:center;
    font-size:42px;
    font-weight:700;
    margin-top:10px;
}

.subtitle{
    text-align:center;
    color:#9ca3af;
    font-size:20px;
    margin-bottom:40px;
}

.upload-box{
    border:1px solid #2f2f2f;
    border-radius:18px;
    padding:20px;
    margin-top:20px;
}

.result-card{
    border:1px solid #2f2f2f;
    border-radius:18px;
    padding:20px;
}

</style>
""",
unsafe_allow_html=True)


with open(
    "logo.png",
    "rb"
) as img_file:

    logo_base64 = base64.b64encode(
        img_file.read()
    ).decode()


st.markdown(
    f"""
    <div class="logo-container">
        <img src="data:image/png;base64,{logo_base64}">
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="main-title">
    
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="subtitle">
        Detección de cáncer pulmonar a través de un TAC mediante Inteligencia Artificial
    </div>
    """,
    unsafe_allow_html=True
)

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "confidence" not in st.session_state:
    st.session_state.confidence = None

if "report" not in st.session_state:
    st.session_state.report = None

if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None

if "heatmap_path" not in st.session_state:
    st.session_state.heatmap_path = None

if "overlay_path" not in st.session_state:
    st.session_state.overlay_path = None

if "last_file" not in st.session_state:
    st.session_state.last_file = None



st.markdown(
    """
    ### ¿Qué TAC deseas analizar?
    """
)

uploaded_file = st.file_uploader(
    "Sube un TAC de tórax",
    type=["png", "jpg", "jpeg"],
    help="Subir • PNG • JPG • JPEG • Máximo 200 MB"
)



col1, col2 = st.columns(2)

with col1:

    analizar = st.button(
        "Analizar imagen",
        use_container_width=True
    )

with col2:

    if st.session_state.analysis_done:

        with open(
            st.session_state.pdf_path,
            "rb"
        ) as pdf_file:

            pdf_bytes = pdf_file.read()

        st.download_button(
            "Descargar PDF",
            pdf_bytes,
            file_name="lungvision_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )



if uploaded_file is not None:

    if st.session_state.last_file != uploaded_file.name:

        st.session_state.analysis_done = False
        st.session_state.prediction = None
        st.session_state.confidence = None
        st.session_state.report = None
        st.session_state.pdf_path = None
        st.session_state.heatmap_path = None
        st.session_state.overlay_path = None

        st.session_state.last_file = uploaded_file.name

    image = Image.open(
        uploaded_file
    )

    image.save(
        "outputs/original_ct.png"
    )

    st.image(
        image,
        caption="TAC cargado",
        use_container_width=True
    )

    if analizar:

        with st.spinner(
            "Validando TAC..."
        ):

            lung_result, _ = is_lung_xray(
                image
            )

        if lung_result == "NOT_LUNG_XRAY":

            st.error(
                "La imagen no parece ser un TAC pulmonar."
            )

            st.stop()

        with st.spinner(
            "Ejecutando modelo de IA..."
        ):

            prediction, confidence = predict(
                image
            )

        with st.spinner(
            "Generando Grad-CAM..."
        ):

            heatmap_path, overlay_path = generate_gradcam(
                image
            )

        with st.spinner(
            "Cargando..."
        ):

            report = generate_llm_report(
                prediction,
                confidence
            )

        with st.spinner(
            "Generando PDF..."
        ):

            pdf_path = create_pdf(
                prediction,
                confidence,
                report,
                "outputs/original_ct.png",
                heatmap_path,
                overlay_path
            )

        st.session_state.prediction = prediction
        st.session_state.confidence = confidence
        st.session_state.report = report
        st.session_state.pdf_path = pdf_path
        st.session_state.heatmap_path = heatmap_path
        st.session_state.overlay_path = overlay_path
        st.session_state.analysis_done = True

        if st.session_state.analysis_done:

            st.markdown("---")

            st.subheader("Resultado generado por IA")

            with st.container():

                if (
                    st.session_state.prediction=="CÁNCER"
                    or
                    st.session_state.prediction=="CÁNCER"

                ):
                    
                    st.error(
                        f"Resultado: {st.session_state.prediction}"
                    )

                else:
                    st.success(
                        f"Resultado:{st.session_state.prediction}"
                    )

                    st.metric(
                        "Confianza",
                        f"{st.session_state.confidence:.2f}%"
                    )

                st.markdown("---")

                st.subheader(
                    "Grad-CAM"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.image(
                        st.session_state.heatmap_path,
                        caption="Mapa de calor",
                        use_container_width=True
                    )

                with col2:

                    st.image(
                    st.session_state.overlay_path,
                    caption="Superposición sobre el TAC",
                    use_container_width=True
                    )


                st.markdown("---")


                st.subheader(
                    "Informe Médico Generado por IA 📋"
                )

                st.info(
                    st.session_state.report
                )


                st.markdown("---")


                st.subheader(
                    "Informe PDF 📄"
                )

                with open(
                    st.session_state.pdf_path,
                    "rb"
                ) as pdf_file:

                    pdf_bytes = pdf_file.read()

                st.download_button(
                label="Descargar informe PDF",
                data=pdf_bytes,
                file_name="lungvision_report.pdf",
                mime="application/pdf",
                use_container_width=True
                )


                st.markdown("---")


                st.success(
                    " Análisis completado correctamente ✅"
                )

