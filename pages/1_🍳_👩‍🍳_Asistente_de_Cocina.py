import streamlit as st
from openai import OpenAI

# ── CONFIGURACIÓN ─────────────────────────────
st.set_page_config(
    page_title="Asistente de Cocina Virtual",
    page_icon="🍳",
    layout="centered"
)

# ── ESTILOS ───────────────────────────────────
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to bottom right, #dbeafe, #93c5fd);
}

[data-testid="stSidebar"] {
    background-color: #dbeafe;
}

h1, h2, h3, p, span, label {
    color: #1E3A8A !important;
    font-family: 'Trebuchet MS', sans-serif;
}

/* TARJETAS */
.card {
    background-color: rgba(255,255,255,0.80);
    padding: 25px;
    border-radius: 25px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.15);
}

/* BOTONES */
div.stButton > button {
    background-color: #3B82F6 !important;
    color: white !important;
    border-radius: 20px !important;
    border: none !important;
    width: 100%;
    font-weight: bold;
}

/* CHAT */
.stChatMessage {
    background-color: rgba(255,255,255,0.85);
    border-radius: 20px;
    border: 1px solid #E2E8F0;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────
st.markdown("""
# 🍳🧑‍🍳 Asistente de Cocina Virtual

### Descubre recetas deliciosas utilizando los ingredientes que tienes disponibles 💙
""")

# ── TARJETA BIENVENIDA ───────────────────────
st.markdown("""
<div class="card">

<h3>👩‍🍳 Bienvenido a SmartKitchen AI</h3>

<p>
¡Hola! Soy tu chef personal. Dime qué ingredientes tienes y crearemos algo increíble juntos ✨
</p>

</div>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────
with st.sidebar:

    st.header("⚙️ Configuración")

    api_key = st.text_input(
        "🔑 OpenAI API Key",
        type="password",
        placeholder="sk-..."
    )

    model = st.selectbox(
        "Modelo",
        ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
    )

    if "system_prompt" not in st.session_state:

        st.session_state.system_prompt = (
            "Eres un chef profesional alegre, creativo y experto en optimizar "
            "ingredientes."
        )

# ── HISTORIAL ─────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ── INPUT ─────────────────────────────────────
if prompt := st.chat_input("🍳 Escribe tus ingredientes o dudas culinarias..."):

    if not api_key:

        st.warning("Por favor ingresa tu API Key.")
        st.stop()

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    messages_to_send = [
        {
            "role": "system",
            "content": st.session_state.system_prompt
        }
    ]

    messages_to_send += st.session_state.messages

    client = OpenAI(api_key=api_key)

    with st.chat_message("assistant"):

        with st.spinner("🍳 Cocinando una respuesta..."):

            try:

                response = client.chat.completions.create(
                    model=model,
                    messages=messages_to_send,
                )

                reply = response.choices[0].message.content

                st.write(reply)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })

            except Exception as e:

                st.error(f"Error: {e}")

# ── LIMPIAR CHAT ──────────────────────────────
if st.session_state.messages:

    st.write("---")

    if st.button("🗑️ Limpiar conversación"):

        st.session_state.messages = []

        st.rerun()
