import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Asistente de Cocina", page_icon="🍳", layout="wide")

st.markdown("# 🍳 Asistente de Cocina con IA Real")
st.write("Escribe libremente los ingredientes que tienes en tu nevera y nuestra IA creará una receta real y coherente en segundos.")
st.write("---")

# 🔐 CLAVE API DE GOOGLE AI STUDIO (Tu clave del proyecto)
API_KEY = "AIzaSyBGng7EBh0dKFD53KXz7cOapi5e4Pjlp9Q"

try:
    genai.configure(api_key=API_KEY)
    # Usamos el nombre de modelo calificado completo para evitar errores de versión
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception as e:
    st.error(f"Error al conectar con la IA de Google: {e}")

# Inicializar el historial del chat en la memoria de la aplicación si no existe
if "chat_conversacional_real" not in st.session_state:
    st.session_state["chat_conversacional_real"] = [
        {"role": "assistant", "content": "¡Hola! Soy tu chef SmartKitchen. Dime qué ingredientes tienes a la mano hoy y te diseñaré una receta real y lógica con ellos."}
    ]

col1, col2 = st.columns([1, 1.8], gap="large")

with col1:
    st.subheader("🛒 ¿Qué tienes en tu nevera?")
    
    # Caja de entrada de texto libre
    ingredientes = st.text_input(
        "Ingresa tus ingredientes:", 
        placeholder="Ej: huevos, pan, leche, queso",
        key="input_ingredientes_real"
    )

    if st.button("✨ Generar Receta Personalizada", type="primary", use_container_width=True):
        if ingredientes:
            # Registrar lo que puso el usuario en la interfaz del chat
            st.session_state["chat_conversacional_real"].append({"role": "user", "content": f"Tengo: {ingredientes}"})
            
            with st.spinner("El Chef de IA está analizando tus ingredientes..."):
                try:
                    # Le damos un rol (prompt) claro a la IA para que razone culinariamente
                    prompt_chef = (
                        f"Actúa como un chef profesional y creativo. El usuario te da estos ingredientes: '{ingredientes}'. "
                        f"Crea una receta real, lógica y deliciosa que tenga sentido estricto con lo que te acaban de dar. "
                        f"No uses plantillas fijas. Si te dan ingredientes de desayuno (como huevos y leche), haz una receta de desayuno coherente; si te dan carne y arroz, haz un almuerzo. "
                        f"Estructura la respuesta de forma limpia usando títulos con emojis: 👨‍🍳 Nombre del Plato, 🛒 Ingredientes a Utilizar y 📝 Paso a Paso bien redactado. "
                        f"Al final de todo, añade esta frase exacta como consejo de diseño IoT: '💡 Consejo de Diseño UX: Recuerda que si este plato genera vapores o humos intensos, puedes ir a la pestaña Alertas y Tiempos para encender el extractor remoto en Wokwi.'"
                    )
                    
                    # Generación de contenido real a través de internet
                    respuesta = model.generate_content(prompt_chef)
                    
                    # Guardar la respuesta inteligente de la IA en el historial
                    st.session_state["chat_conversacional_real"].append({"role": "assistant", "content": respuesta.text})
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Hubo un problema con la API de Google: {e}")
        else:
            st.warning("Escribe al menos un ingrediente para poder ayudarte.")

with col2:
    st.subheader("💬 Menú y Sugerencias del Chef")
    
    # Renderizar el historial en formato chat dinámico de Streamlit
    for msg in st.session_state["chat_conversacional_real"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Botón para limpiar la conversación si ya hay mensajes
    if len(st.session_state["chat_conversacional_real"]) > 1:
        st.write("---")
        if st.button("🧹 Limpiar historial de recetas", use_container_width=True):
            st.session_state["chat_conversacional_real"] = [
                {"role": "assistant", "content": "¡Listo! Todo despejado. ¿Qué otros ingredientes tienes para probar hoy?"}
            ]
            st.rerun()
