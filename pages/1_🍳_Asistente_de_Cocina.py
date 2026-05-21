import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Mi propio chat", page_icon="💬", layout="centered")

# ── Sidebar ──────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuración")

    api_key = st.text_input("🔑 OpenAI API Key", type="password", placeholder="sk-...")

    model = st.selectbox("Modelo", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"])

    st.divider()

    st.subheader("🤖 Personalidad")

    if "system_prompt" not in st.session_state:
        st.session_state.system_prompt = ""

    system_input = st.text_area(
        "System Prompt",
        value=st.session_state.system_prompt,
        placeholder="Ej: Eres un asistente muy gracioso, responde siempre con algo gracioso.",
        height=180,
        label_visibility="collapsed"
    )

    if st.button("💾 Guardar personalidad", use_container_width=True):
        st.session_state.system_prompt = system_input
        st.success("¡Guardado!")

    if st.session_state.system_prompt:
        st.caption(f"✅ Activo: *{st.session_state.system_prompt[:60]}...*" 
                   if len(st.session_state.system_prompt) > 60 
                   else f"✅ Activo: *{st.session_state.system_prompt}*")

# ── Main ─────────────────────────────────────────────────
st.title("💬 Mi propio Chat")

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input del usuario
if prompt := st.chat_input("Escribe un mensaje..."):
    if not api_key:
        st.warning("Por favor ingresa tu API Key en el panel lateral.")
        st.stop()

    # Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Construir lista de mensajes con system prompt
    messages_to_send = []
    if st.session_state.system_prompt:
        messages_to_send.append({"role": "system", "content": st.session_state.system_prompt})
    messages_to_send += st.session_state.messages

    # Llamar a OpenAI
    client = OpenAI(api_key=api_key)
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
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

# Botón limpiar
if st.session_state.messages:
    if st.button("🗑️ Limpiar conversación"):
        st.session_state.messages = []
        st.rerun()
