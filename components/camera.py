import streamlit as st

def render_camera_component() -> bytes:
    st.markdown("### 🎥 Entrada de Imagem em Tempo Real")
    # Captura nativa do Streamlit acionando os drivers da câmera do sistema cliente
    img_file = st.camera_input("Alinhe a captura de imagem no visor abaixo:")
    if img_file is not None:
        return img_file.getvalue()
    return None