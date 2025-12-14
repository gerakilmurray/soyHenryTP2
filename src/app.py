"""
Interfaz gráfica web usando Streamlit.
Proporciona una UI moderna y fácil de usar para el sistema de atención al cliente.
"""
import streamlit as st
import sys
from pathlib import Path
import logging

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent import CustomerServiceAgent
from src.router import QueryType

# Configurar página
st.set_page_config(
    page_title="BANCO HENRY - Atención al Cliente",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurar logging
logging.basicConfig(level=logging.INFO)


# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .query-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .response-box {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    
    .stat-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_agent():
    """Inicializa el agente (con caché para no reinicializar)."""
    with st.spinner("🔄 Inicializando el sistema..."):
        return CustomerServiceAgent()


def display_header():
    """Muestra el encabezado de la aplicación."""
    st.markdown('<h1 class="main-header">🏦 BANCO HENRY<br>Sistema de Atención al Cliente</h1>', unsafe_allow_html=True)
    st.markdown("---")


def display_sidebar():
    """Muestra la barra lateral con información y estadísticas."""
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/667eea/ffffff?text=BANCO+HENRY", use_container_width=True)
        
        st.markdown("### 📋 Acerca del Sistema")
        st.info("""
        Este sistema utiliza Inteligencia Artificial para atender tus consultas bancarias de forma automatizada.
        
        **Capacidades:**
        - 💰 Consultar balances de cuenta
        - 📚 Información sobre servicios bancarios
        - 💬 Responder preguntas generales
        """)
        
        st.markdown("### 🎯 Ejemplos de Consultas")
        
        with st.expander("💰 Balance"):
            st.code("¿Cuál es el balance de la cédula V-12345678?")
            st.code("Consultar saldo V-91827364")
        
        with st.expander("📚 Información Bancaria"):
            st.code("¿Cómo abrir una cuenta de ahorros?")
            st.code("¿Cómo solicitar una tarjeta de crédito?")
        
        with st.expander("💬 Generales"):
            st.code("¿Qué servicios ofrecen?")
            st.code("Horarios de atención")
        
        st.markdown("---")
        
        # Estadísticas
        if 'agent' in st.session_state:
            st.markdown("### 📊 Estadísticas")
            stats = st.session_state.agent.get_statistics()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total", stats['total_queries'])
                st.metric("Balance", stats['balance_queries'])
            with col2:
                st.metric("Conocimiento", stats['knowledge_queries'])
                st.metric("Generales", stats['general_queries'])
        
        st.markdown("---")
        st.markdown("### ⚙️ Tecnologías")
        st.markdown("""
        - **LangChain** - Orquestación
        - **OpenAI GPT-4** - LLM
        - **FAISS** - Base vectorial
        - **Streamlit** - Interfaz web
        """)


def get_query_type_emoji(query_type: str) -> str:
    """Retorna el emoji según el tipo de consulta."""
    emoji_map = {
        "balance": "💰",
        "knowledge": "📚",
        "general": "💬",
        "error": "❌"
    }
    return emoji_map.get(query_type, "💬")


def display_response(result: dict):
    """Muestra la respuesta del sistema."""
    emoji = get_query_type_emoji(result.get("query_type", "general"))
    query_type = result.get("query_type", "general").upper()
    
    st.markdown(f"### {emoji} Respuesta ({query_type})")
    
    if result.get("success", False):
        st.markdown('<div class="response-box">', unsafe_allow_html=True)
        st.markdown(result["response"])
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Información adicional para balance
        if result.get("query_type") == "balance" and "data" in result:
            data = result["data"]
            if data.get("found"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Titular", data["nombre"])
                with col2:
                    st.metric("Cédula", data["cedula"])
                with col3:
                    st.metric("Balance", f"${data['balance']:,.2f}")
        
        # Documentos fuente para knowledge
        if result.get("query_type") == "knowledge" and "source_documents" in result:
            with st.expander("📄 Ver fuentes de información"):
                for i, doc in enumerate(result["source_documents"], 1):
                    st.markdown(f"**Fuente {i}:** {Path(doc['source']).name}")
                    st.text(doc['content'][:200] + "...")
                    st.markdown("---")
    else:
        st.error(result["response"])


def main():
    """Función principal de la aplicación."""
    display_header()
    display_sidebar()
    
    # Inicializar session state
    if 'agent' not in st.session_state:
        try:
            st.session_state.agent = initialize_agent()
            st.success("✅ Sistema inicializado correctamente!")
        except Exception as e:
            st.error(f"❌ Error al inicializar el sistema: {e}")
            st.stop()
    
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    # Área principal
    st.markdown("### 💬 Realiza tu consulta")
    
    # Input de consulta
    query = st.text_input(
        "Escribe tu pregunta aquí:",
        placeholder="Ejemplo: ¿Cuál es el balance de la cédula V-12345678?",
        key="query_input"
    )
    
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        submit_button = st.button("🚀 Consultar", type="primary", use_container_width=True)
    
    with col2:
        clear_button = st.button("🗑️ Limpiar", use_container_width=True)
    
    # Procesar consulta
    if submit_button and query:
        with st.spinner("🤔 Procesando tu consulta..."):
            result = st.session_state.agent.process_query(query)
            
            # Agregar a historial
            st.session_state.history.insert(0, {
                "query": query,
                "result": result
            })
            
            # Mostrar respuesta
            display_response(result)
    
    # Limpiar historial
    if clear_button:
        st.session_state.history = []
        st.session_state.agent.reset_statistics()
        st.rerun()
    
    # Mostrar historial
    if st.session_state.history:
        st.markdown("---")
        st.markdown("### 📜 Historial de Consultas")
        
        for i, item in enumerate(st.session_state.history[:10], 1):  # Últimas 10
            with st.expander(f"{i}. {item['query'][:100]}..."):
                st.markdown(f"**Consulta:** {item['query']}")
                st.markdown("**Respuesta:**")
                st.info(item['result']['response'])
                st.caption(f"Tipo: {item['result']['query_type']}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>🏦 BANCO HENRY - Sistema de Atención al Cliente Automatizado</p>
        <p>Powered by LangChain & OpenAI GPT-4 | Desarrollado con ❤️ usando Streamlit</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
