import streamlit as st
from streamlit_mic_recorder import mic_recorder
import time

st.set_page_config(page_title="Asistente de Voz", page_icon="🎙️", layout="wide")

st.markdown("# 🎙️ Asistente de Voz & Co-Creación")
st.write("Dita los ingredientes que tienes en tu nevera y el asistente te propondrá una receta.")
st.write("---")

col1, col2 = st.columns([1, 1.5], gap="large")

with col1:
    st.subheader("¿Qué tienes en la nevera?")
    st.write("Presiona el botón y menciona de 3 a 4 ingredientes:")
    
    audio = mic_recorder(
        start_prompt="🎙️ Dictar Ingredientes",
        stop_prompt="🛑 Terminar Lista",
        just_once=False,
        key="mic_cocina"
    )

    # Simulación de procesamiento de la intención del usuario
    if audio:
        st.audio(audio['bytes'], format='audio/wav')
        
        with st.spinner("Procesando ingredientes con IA..."):
            time.sleep(2.5) # Simula el tiempo de respuesta de la API
            
        st.success("¡Ingredientes detectados con éxito!")
        
        # Guardamos en el estado que encontramos ingredientes simulados
        st.session_state["ingredientes_listos"] = True
    else:
        if "ingredientes_listos" not in st.session_state:
            st.session_state["ingredientes_listos"] = False

with col2:
    st.subheader("💡 Receta Sugerida")
    
    if st.session_state["ingredientes_listos"]:
        st.markdown("### 👨‍🍳 Pollo Cremoso al Tomate Estilo SmartKitchen")
        st.caption("Receta generada en base a: *Pollo, Tomate, Cebolla y Crema de leche*")
        
        tab1, tab2 = st.tabs(["🛒 Lista Ajustada", "📝 Preparación"])
        
        with tab1:
            st.markdown("""
            * **Tus ingredientes:** Pollo (pechuga en cubos), Tomates maduros, Cebolla picada, Crema de leche.
            * **Básicos de despensa necesarios:** Aceite de oliva, sal, pimienta y un toque de ajo.
            """)
            
        with tab2:
            st.markdown("""
            1.  **Sofreír:** En una sartén con aceite de oliva, dora la cebolla picada y un toque de ajo hasta que estén transparentes.
            2.  **Dorar la proteína:** Sella los cubos de pollo sazonados con sal y pimienta hasta que cambien de color.
            3.  **Crear la salsa:** Agrega los tomates licuados o picados finamente y deja reducir a fuego medio por 5 minutos.
            4.  **Textura:** Baja el fuego al mínimo, vierte la crema de leche, revuelve bien y cocina por 3 minutos más hasta lograr una consistencia cremosa. ¡Sirve caliente!
            """)
            
        st.info("💡 **Tip del asistente:** Puedes enviarle una señal a tu Wokwi para prender el extractor si notas que el sofrito genera mucho humo.")
    else:
        st.info("Usa el micrófono de la izquierda para listar tus alimentos y ver la magia.")
