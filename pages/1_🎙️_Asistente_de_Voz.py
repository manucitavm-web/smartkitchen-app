import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Asistente de Cocina", page_icon="💬", layout="wide")

st.markdown("# 💬 Asistente de Cocina con IA Real")
st.write("Escribe libremente los ingredientes que tienes en tu nevera y nuestro Chef de IA te diseñará una receta única en segundos.")
st.write("---")

# 🔐 CONFIGURACIÓN DE LA IA (Pega aquí tu clave larga de Google AI Studio que empieza con AIzaSy)
API_KEY = "TU_API_KEY_AQUÍ"

if API_KEY != "AIzaSyBGng7EBh0dKFD53KXz7cOapi5e4Pjlp9Q":
    try:
        genai.configure(api_key=API_KEY)
        # Usamos el modelo oficial y más estable de la librería actual
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Error al inicializar el modelo de IA: {e}")
else:
    st.warning("⚠️ Recuerda pegar tu API Key de Google AI Studio en la línea 11 del código para que la IA pueda responder.")

# Inicializar el historial del chat en la memoria de la aplicación si no existe
if "historial_chat_cocina" not in st.session_state:
    st.session_state["historial_chat_cocina"] = [
        {"role": "assistant", "content": "¡Hola! Soy tu chef SmartKitchen. Cuéntame qué ingredientes tienes en tu nevera hoy y te armaré un menú a la medida."}
    ]

# Renderizar el historial de mensajes de forma estética (estilo chat real)
for mensaje in st.session_state["historial_chat_cocina"]:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# Cuadro de entrada de texto al final de la pantalla (estilo chat de mensajería)
if usuario_input := st.chat_input("Ej: Tengo pollo, papas, cebolla y crema de leche..."):
    
    # 1. Mostrar de inmediato lo que escribió el usuario en la pantalla
    with st.chat_message("user"):
        st.markdown(usuario_input)
    
    # Guardar en la memoria del historial
    st.session_state["historial_chat_cocina"].append({"role": "user", "content": usuario_input})
    
    # 2. Generar la respuesta real con la IA
    if API_KEY != "TU_API_KEY_AQUÍ":
        with st.chat_message("assistant"):
            with st.spinner("El Chef de IA está pensando tu receta..."):
                try:
                    # Diseñamos un prompt con enfoque UX para que la respuesta de la IA sea hermosa y estructurada
                    prompt_instruccion = (
                        f"Actúa como un chef profesional de asistencia en el hogar. El usuario te dice lo siguiente: '{usuario_input}'. "
                        f"Diseña una receta creativa, rápida y deliciosa usando principalmente los ingredientes que te mencionan y básicos de despensa (sal, aceite, agua). "
                        f"Estructura tu respuesta usando títulos claros (👨‍🍳 Nombre del Plato, 🛒 Ingredientes Necesarios, 📝 Paso a Paso). "
                        f"Al final, añade un consejo breve que sugiera al usuario monitorear los sensores de la cocina si nota que la temperatura sube mucho."
                    )
                    
                    # Llamada a la API de Google
                    respuesta = model.generate_content(prompt_instruccion)
                    
                    # Mostrar la receta en la pantalla
                    st.markdown(respuesta.text)
                    
                    # Guardar la receta en la memoria del historial
                    st.session_state["historial_chat_cocina"].append({"role": "assistant", "content": respuesta.text})
                    
                except Exception as e:
                    st.error(f"Hubo un problema al conectar con el servidor de Google: {e}")
                    st.info("Tip técnico: Revisa que tu clave API esté bien copiada y no tenga espacios extra.")
    else:
        st.error("No puedo generar la receta porque aún no has puesto tu API Key en la línea 11.")

# Botón flotante en la barra lateral para limpiar el chat si se desea empezar de nuevo
with st.sidebar:
    st.markdown("### Configuración del Asistente")
    if st.button("🧹 Limpiar historial del Chat"):
        st.session_state["historial_chat_cocina"] = [
            {"role": "assistant", "content": "¡Listo! Todo borrado. ¿Qué nuevos ingredientes tienes hoy?"}
        ]
        st.rerun()
