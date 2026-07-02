import os
import streamlit as st
import pandas as pd
from PIL import Image
from utils.helpers import converter_para_csv, converter_para_json

def render_history_component(dados: list, controller):
    st.subheader("📜 Repositório e Histórico das Análises")
    
    if not dados:
        st.info("Sem registros no histórico.")
        return

    # Barra de Ferramentas de Filtragem e Exportação
    col_search, col_date = st.columns(2)
    with col_search:
        search_query = st.text_input("🔍 Filtrar por objetos ou descrição:")
    with col_date:
        filtro_data = st.text_input("📅 Filtrar por Data (DD/MM/AAAA):")

    # Filtragem dos dados na camada View
    dados_filtrados = dados
    if search_query:
        dados_filtrados = [d for d in dados_filtrados if search_query.lower() in str(d['descricao']).lower() or search_query.lower() in str(d['objetos']).lower()]
    if filtro_data:
        dados_filtrados = [d for d in dados_filtrados if filtro_data in str(d['created_at'])]

    # Botões de Exportação Global
    csv_data = converter_para_csv(dados_filtrados)
    json_data = converter_para_json(dados_filtrados)
    
    c_exp1, c_exp2 = st.columns(2)
    with c_exp1:
        st.download_button("📥 Exportar CSV", data=csv_data, file_name="historico_cv.csv", mime="text/csv")
    with c_exp2:
        st.download_button("📥 Exportar JSON", data=json_data, file_name="historico_cv.json", mime="application/json")

    st.markdown("---")

    # Renderização da Lista Dinâmica (Cards)
    for idx, item in enumerate(dados_filtrados):
        with st.container():
            col_img, col_info, col_actions = st.columns([1.5, 3, 2.5])
            
            with col_img:
                if os.path.exists(item['image_path']):
                    img = Image.open(item['image_path'])
                    st.image(img, use_container_width=True)
                    # Botão para Download individual da imagem física
                    with open(item['image_path'], "rb") as f:
                        st.download_button("Download Img", data=f.read(), file_name=f"img_{item['id']}.jpg", mime="image/jpeg", key=f"dl_{item['id']}")
                else:
                    st.warning("Arquivo físico não localizado.")
                    
            with col_info:
                st.markdown(f"**Registro ID:** #{item['id']} | **Data:** {item['created_at']}")
                st.markdown(f"**Descrição:** {item['descricao']}")
                st.markdown(f"**Luminosidade:** {item['luminosidade']} | **Nitidez:** {item['nitidez']}")
                st.markdown(f"**Cores Predominantes:** {item['cores']}")
                st.markdown(f"**Pessoas/Rostos:** {item['quantidade_pessoas']}")
                if item['transcricao']:
                    st.info(f"🎙️ **Transcrição:** {item['transcricao']}")
                else:
                    st.caption("Sem notas de áudio vinculadas.")

            with col_actions:
                st.markdown("**Ações do Registro:**")
                # Botão Excluir Registro Geral
                if st.button("❌ Remover Registro", key=f"del_reg_{item['id']}"):
                    if controller.deletar_registro(item['id']):
                        st.success("Excluído!")
                        st.rerun()

                # Gestão de Áudio Retrospectiva
                st.markdown("---")
                audio_bytes_vinc = st.audio_input("Vincular/Atualizar Áudio:", key=st.write = f"aud_vinc_{item['id']}")
                if audio_bytes_vinc is not None:
                    if st.button("💾 Salvar Novo Áudio", key=f"save_aud_{item['id']}"):
                        controller.gerenciar_audio_registro(item['id'], audio_bytes_vinc, "vincular")
                        st.success("Áudio Transcrito e Salvo!")
                        st.rerun()
                
                if item['transcricao']:
                    if st.button("🗑️ Remover Apenas Áudio", key=f"del_aud_{item['id']}"):
                        controller.gerenciar_audio_registro(item['id'], None, "excluir")
                        st.success("Áudio removido!")
                        st.rerun()
            st.markdown("<hr style='border:1px dashed #777'>", unsafe_allowed_html=True)