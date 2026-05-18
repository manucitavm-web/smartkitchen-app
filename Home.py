import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="SmartKitchen",
    page_icon="🍳",
    layout="wide"
)

st.title("🍳 SmartKitchen Home Assistant")

st.markdown("""
## Bienvenido a SmartKitchen

Una cocina inteligente multimodal que permite:
- 🍳 Asistente de Cocina Inteligente
- 🌡️ Monitoreo de sensores desde el simulador Wokwi
- ⏱️ Temporizadores y alertas en la nube
- 🖼️ Procesamiento de imágenes con Pillow
""")

# Carga de la imagen directamente desde la raíz del repositorio
try:
    img = Image.open("cocina.jpg")  # Modificado para buscar en la raíz
    st.image(img, caption="Centro de Control Integrado", use_container_width=True)
except FileNotFoundError:
    # Imagen de respaldo automática si aún no has subido tu archivo 'kitchen.jpeg'
    st.image("https://images.unsplash.com/photo-1556911220-e15b29be8c8f", caption="Ecosistema SmartKitchen conectado", use_container_width=True)

st.info("Usa el menú lateral para navegar entre páginas.")
