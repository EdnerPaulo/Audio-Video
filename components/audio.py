import streamlit as st

def render_audio_component(key: str = "main_audio") -> bytes:
    st.markdown("### 🎙️ Entrada de Notas de Áudio / Observações")
    # Gravador nativo ou upload de áudio gratuito
    audio_file = st.file_detector = st.audio_input("Grave sua observação por voz:", key=key)
    if audio_file is not None:
        return audio_file.getvalue()
    return None