import streamlit as st
from openai import OpenAI

# ── CONFIGURACIÓN INICIAL ────────────────────────────────
st.set_page_config(page_title="Asistente de Cocina Virtual", page_icon="💬", layout="centered")

# ── ESTÉTICA UNIFICADA (AZUL) ─────────────────────────────
st.markdown("""
    <style>
    /* Fondo de la página en un gris azulado limpio */
    .main { background-color: #F4F6F9; }
    
    /* Títulos y textos en azul oscuro elegante */
    h1, h2, h3, p, span, label { color: #1E3A8A !important; }

    /* Estilo para los botones (Guardar, Limpiar, etc.) */
    div.stButton > button {
        background-color: #3B82F6 !important;
        color: white !important;
        border-radius: 20px !important;
        border: 2px solid #60A5FA !important;
        width: 100%;
        font-weight: bold;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        background-color: #1D4ED8 !important;
        border: 2px solid #2563EB !important;
        transform: scale(1.02);
    }

    /* Personalización del área de chat */
    .stChatMessage {
        background-color: #FFFFFF;
        border-radius: 15px;
        border: 1px solid #E2E8F0;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ── SIDEBAR (CONFIGURACIÓN) ──────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuración")

    api_key = st.text_input("🔑 OpenAI API Key", type="password", placeholder="sk-...")

    model = st.selectbox("Modelo", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"])

    # 🤫 LÓGICA OCULTA DE PERSONALIDAD: 
    # El prompt se configura en el fondo para la IA, pero ya no se renderiza visualmente en la barra lateral.
    if "system_prompt" not in st.session_state:
        st.session_state.system_prompt = (
            "Eres un chef profesional alegre, creativo y experto en optimizar "
            "ingredientes. Tu objetivo es ayudar a los usuarios a crear recetas deliciosas "
            "con lo que tengan en su nevera. Habla con entusiasmo, da tips de cocina "
            "y usa emojis relacionados con alimentos."
        )

# ── MAIN (INTERFAZ DE CHAT) ─────────────────────────────
st.title("🍳🧑‍🍳 Asistente de Cocina Virtual")
st.write("¡Hola! Soy tu chef personal. Dime qué ingredientes tienes y crearemos algo increíble juntos.")
st.write("---")

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial con burbujas de chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input del usuario
if prompt := st.chat_input("Escribe tus ingredientes o dudas culinarias..."):
    if not api_key:
        st.warning("Por favor ingresa tu API Key en el panel lateral.")
        st.stop()

    # Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Construir lista de mensajes con el system prompt activo
    messages_to_send = []
    if st.session_state.system_prompt:
        messages_to_send.append({"role": "system", "content": st.session_state.system_prompt})
    messages_to_send += st.session_state.messages

    # Llamar a OpenAI
    client = OpenAI(api_key=api_key)
    with st.chat_message("assistant"):
        with st.spinner("Cocinando una respuesta..."):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages_to_send,
                )
                reply = response.choices[0].message.content
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")

# Botón para limpiar la mesa (conversación)
if st.session_state.messages:
    st.write("---")
    if st.button("🗑️ Limpiar conversación"):
        st.session_state.messages = []
        st.rerun()
