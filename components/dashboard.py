import streamlit as st
import pandas as pd

def render_dashboard(dados: list):
    st.subheader("📊 Painel Analítico das Capturas")
    if not dados:
        st.info("Nenhum dado analítico coletado até o momento.")
        return

    df = pd.DataFrame(dados)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Análises", len(df))
    with col2:
        st.metric("Rostos Detectados (Acumulado)", int(df['rostos'].sum()))
    with col3:
        # Média da quantidade de pessoas registradas por frame
        st.metric("Média de Pessoas/Foto", f"{df['quantidade_pessoas'].mean():.1f}")
        
    st.markdown("---")