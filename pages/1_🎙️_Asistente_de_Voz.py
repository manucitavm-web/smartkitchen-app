import streamlit as st
import time
import random

st.set_page_config(page_title="Asistente de Cocina", page_icon="🍳", layout="wide")

st.markdown("# 🍳 Asistente de Cocina Inteligente")
st.write("Escribe libremente los ingredientes de tu nevera para diseñar una receta instantánea.")
st.write("---")

# Inicializar el historial del chat en la memoria de la aplicación
if "chat_廚房" not in st.session_state:
    st.session_state["chat_廚房"] = [
        {"role": "assistant", "content": "¡Hola! Soy tu asistente SmartKitchen. Dime qué ingredientes tienes en tu nevera hoy (puedes separarlos por espacios o comas) y te armaré una receta a la medida de inmediato."}
    ]

col1, col2 = st.columns([1, 1.8], gap="large")

with col1:
    st.subheader("🛒 ¿Qué tienes a la mano?")
    
    # Entrada libre y directa de texto
    ingredientes = st.text_input(
        "Lista de Ingredientes:", 
        placeholder="Ej: carne tomate arroz plátano",
        key="input_ingredientes"
    )

    if st.button("✨ Generar Receta Personalizada", type="primary", use_container_width=True):
        if ingredientes:
            # Registrar el mensaje del usuario en el chat
            st.session_state["chat_廚房"].append({"role": "user", "content": f"Tengo: {ingredientes}"})
            
            with st.spinner("Nuestro chef digital está combinando tus ingredientes..."):
                time.sleep(1.2)  # Simula un tiempo de procesamiento fluido
                
                # Procesamos el texto eliminando comas o espacios para mapear los ingredientes
                texto_limpio = ingredientes.replace(",", " ")
                lista_ingredientes = [i.strip().capitalize() for i in texto_limpio.split(" ") if i.strip() and len(i.strip()) > 1]
                
                if len(lista_ingredientes) == 0:
                    lista_ingredientes = ["Ingredientes Variados"]
                
                # Técnicas de cocina aleatorias para darle variedad al texto generado
                tecnicas = ["un salteado rápido", "un estofado rústico", "un tazón templado estilo bowl", "una cazuela casera"]
                tecnica_elegida = random.choice(tecnicas)
                
                # Estructura de la receta dinámica basada en la entrada real del usuario
                titulo_plato = f"👨‍🍳 {lista_ingredientes[0]} Especial SmartKitchen"
                
                ingredientes_formateados = "\n".join([f"* **{ing}** (Detectado desde tu entrada)." for ing in lista_ingredientes])
                
                pasos_dinamicos = f"1.  **Preparación base:** Toma el ingrediente principal (**{lista_ingredientes[0]}**), pícalo en trozos cómodos y dóralo en una sartén con un chorrito de aceite, sal y pimienta.\n"
                if len(lista_ingredientes) >= 2:
                    pasos_dinamicos += f"2.  **Integración:** Incorpora el segundo ingrediente (**{lista_ingredientes[1]}**) finamente picado para armar una base aromática llena de sabor.\n"
                if len(lista_ingredientes) >= 3:
                    pasos_dinamicos += f"3.  **Complemento técnico:** Suma **{lista_ingredientes[2]}** para aportar textura y cuerpo a la preparación media.\n"
                else:
                    pasos_dinamicos += "3.  **Sazón:** Añade las especias que más te gusten de tu despensa para realzar los aromas.\n"
                
                pasos_dinamicos += f"4.  **Montaje:** Junta todo a fuego medio bajo por 5 minutos adicionales hasta lograr {tecnica_elegida}. ¡Sirve caliente y disfruta!"

                # Respuesta armada dinámicamente con los datos reales del usuario
                respuesta_chef = f"""
### {titulo_plato}
¡Excelente combinación! Con lo que registramos podemos preparar {tecnica_elegida}. Aquí tienes la propuesta estructurada:

#### 🛒 Ingredientes a Utilizar:
{ingredientes_formateados}
* *Básicos de cocina:* Aceite, sal y pimienta.

#### 📝 Modo de Preparación:
{pasos_dinamicos}

---
💡 **Consejo de Diseño UX:** Recuerda que si este plato genera vapores o humos intensos, puedes ir a la pestaña **Alertas y Tiempos** para encender el extractor remoto en Wokwi.
"""
                # Guardar respuesta en el historial
                st.session_state["chat_廚房"].append({"role": "assistant", "content": respuesta_chef})
                st.rerun()
        else:
            st.warning("Escribe al menos un ingrediente para poder ayudarte.")

with col2:
    st.subheader("💬 Menú y Sugerencias del Asistente")
    
    # Renderizar el historial completo estilo chat
    for msg in st.session_state["chat_廚房"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Botón para limpiar pantalla
    if len(st.session_state["chat_廚房"]) > 1:
        st.write("---")
        if st.button("🧹 Limpiar historial de recetas", use_container_width=True):
            st.session_state["chat_廚房"] = [
                {"role": "assistant", "content": "¡Listo! Todo despejado. ¿Qué otros ingredientes tienes para probar hoy?"}
            ]
            st.rerun()
