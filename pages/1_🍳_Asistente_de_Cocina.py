import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Asistente de Cocina", page_icon="🍳", layout="wide")

st.markdown("# 🍳 Asistente de Cocina con IA Real")
st.write("Escribe libremente los ingredientes que tienes en tu nevera y nuestra IA creará una receta real y coherente en segundos.")
st.write("---")

# 🔐 CLAVE API DE GOOGLE AI STUDIO
# Pega aquí tu clave larga que empieza con "AIzaSy..." para activar la IA real
API_KEY = "AIzaSyBGng7EBh0dKFD53KXz7cOapi5e4Pjlp9Q"

if API_KEY != "TU_API_KEY_AQUÍ":
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Error al conectar con la IA de Google: {e}")
else:
    st.warning("⚠️ Recuerda pegar tu API Key de Google AI Studio en la línea 12 para activar el cerebro de la IA.")

# Inicializar el historial del chat en la memoria si no existe
if "chat_conversacional_real" not in st.session_state:
    st.session_state["chat_conversacional_real"] = [
        {"role": "assistant", "content": "¡Hola! Soy tu chef SmartKitchen. Dime qué ingredientes tienes a la mano hoy y te diseñaré una receta real y lógica con ellos."}
    ]

col1, col2 = st.columns([1, 1.8], gap="large")

with col1:
    st.subheader("🛒 ¿Qué tienes en tu nevera?")
    
    # Caja de texto libre para que el usuario escriba lo que quiera
    ingredientes = st.text_input(
        "Ingresa tus ingredientes:", 
        placeholder="Ej: huevos, pan, leche, queso",
        key="input_ingredientes_real"
    )

    if st.button("✨ Generar Receta Personalizada", type="primary", use_container_width=True):
        if ingredientes:
            # Registrar lo que puso el usuario en la pantalla
            st.session_state["chat_conversacional_real"].append({"role": "user", "content": f"Tengo: {ingredientes}"})
            
            if API_KEY != "TU_API_KEY_AQUÍ":
                with st.spinner("El Chef de IA está analizando tus ingredientes..."):
                    try:
                        # Le damos un rol (prompt) a la IA para que redacte de forma espectacular y coherente
                        prompt_chef = (
                            f"Actúa como un chef profesional y creativo. El usuario te da estos ingredientes: '{ingredientes}'. "
                            f"Crea una receta real, lógica y deliciosa que tenga sentido estricto con lo que te acaban de dar. "
                            f"No uses plantillas fijas. Si te dan ingredientes de desayuno (como huevos y leche), haz una receta de desayuno; si te dan carne, haz un almuerzo. "
                            f"Estructura la respuesta de forma limpia usando títulos emoji: 👨‍🍳 Nombre del Plato, 🛒 Ingredientes y 📝 Paso a Paso bien redactado. "
                            f"Al final de todo, añade esta frase exacta como consejo de diseño IoT: '💡 Consejo de Diseño UX: Recuerda que si este plato genera vapores o humos intensos, puedes ir a la pestaña Alertas y Tiempos para encender el extractor remoto en Wokwi.'"
                        )
                        
                        # Llamada real a la API de Google
                        respuesta = model.generate_content(prompt_chef)
                        
                        # Guardar la respuesta inteligente de la IA en el historial
                        st.session_state["chat_conversacional_real"].append({"role": "assistant", "content": respuesta.text})
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Hubo un problema con la API de Google: {e}")
            else:
                st.error("No puedo generar la receta porque falta tu API Key en la línea 12.")
        else:
            st.warning("Escribe al menos un ingrediente para poder ayudarte.")

with col2:
    st.subheader("💬 Menú y Sugerencias del Chef")
    
    # Renderizar el historial en formato chat dinámico
    for msg in st.session_state["chat_conversacional_real"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Botón para limpiar la conversación
    if len(st.session_state["chat_conversacional_real"]) > 1:
        st.write("---")
        if st.button("🧹 Limpiar historial de recetas", use_container_width=True):
            st.session_state["chat_conversacional_real"] = [
                {"role": "assistant", "content": "¡Listo! Todo despejado. ¿Qué otros ingredientes tienes para probar hoy?"}
            ]
            st.rerun()
