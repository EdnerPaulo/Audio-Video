import streamlit as st
from database.connection import init_db
from controllers.app_controller import AppController
from components.camera import render_camera_component
from components.audio import render_audio_component
from components.dashboard import render_dashboard
from components.history import render_history_component
from config.settings import logger

# Inicialização da Configuração de Página Streamlit
st.set_page_config(
    page_title="Production CV & Audio Pipeline",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar Banco de Dados Automático (Neon.tech)
@st.cache_resource
def startup_db_check():
    init_db()

startup_db_check()

# Inicialização do Controlador Centralizado
controller = AppController()

# --- MENUS VISUAIS ---
st.title("🛡️ Enterprise Computer Vision & Speech to Text Pipeline")

# Menu Lateral (Sidebar)
st.sidebar.title("⚙️ Painel de Controle")
st.sidebar.markdown("---")
st.sidebar.subheader("🔌 Status do Sistema")

# Testador básico de conectividade integrado
if controller is not None:
    st.sidebar.success("Conectado ao PostgreSQL (Neon.tech)")
else:
    st.sidebar.error("Desconectado da infraestrutura central.")

opcao_menu = st.sidebar.radio("Selecione o Módulo Ativo:", ["Captura e Processamento", "Histórico e Analytics"])

# Buscar histórico atualizado para controle de reatividade global
historico_completo = controller.listar_historico()

# --- FLUXO DE OPERAÇÃO 1: CAPTURA ---
if opcao_menu == "Captura e Processamento":
    st.header("📸 Estação Integrada de Coleta")
    
    col_view1, col_view2 = st.columns([1, 1])
    
    with col_view1:
        # Componente Visual da Câmera
        captured_img_bytes = render_camera_component()
        
    with col_view2:
        # Componente de Áudio Simultâneo
        captured_audio_bytes = render_audio_component()

    if captured_img_bytes is not None:
        st.markdown("---")
        st.success("✅ Frame capturado e travado no buffer de memória.")
        
        if st.button("🚀 Processar, Analisar e Persistir Pipeline Completo", use_container_width=True):
            with st.spinner("Executando Inteligência Computacional e Algoritmos de Transcrição..."):
                sucesso, msg = controller.processar_captura(captured_img_bytes, captured_audio_bytes)
                if sucesso:
                    st.balloons()
                    st.success(msg)
                    # Forçar atualização de tela e re-render do histórico de dados
                    st.rerun()
                else:
                    st.error(msg)

# --- FLUXO DE OPERAÇÃO 2: ANALYTICS E HISTÓRICO ---
elif opcao_menu == "Histórico e Analytics":
    # Render Dashboard de Métricas Estáticas/Estatísticas
    render_dashboard(historico_completo)
    
    # Render Lista de Histórico Completo Interativo
    render_history_component(historico_completo, controller)