import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="SmartKitchen",
    page_icon="🍳",
    layout="wide"
)

# ===== ESTILOS =====
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to bottom right, #dbeafe, #93c5fd);
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #dbeafe;
}

/* TARJETAS */
.card {
    background-color: rgba(255,255,255,0.75);
    padding: 25px;
    border-radius: 25px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.15);
}

/* TITULO */
.titulo {
    background: linear-gradient(to right, #60a5fa, #3b82f6);
    padding: 50px;
    border-radius: 30px;
    text-align: center;
    color: white;
    margin-bottom: 30px;
}

.titulo h1 {
    color: white;
    font-size: 60px;
    margin-bottom: 10px;
}

.titulo p {
    color: white;
    font-size: 24px;
}

/* FOOTER */
.footer {
    text-align: center;
    margin-top: 30px;
    color: #1e3a8a;
}

</style>
""", unsafe_allow_html=True)

# ===== HERO =====
st.markdown("""
<div class="titulo">
    <h1>🍳 SmartKitchen</h1>
    <p>
        Disfruta de tu cocina inteligente a través de una gran experiencia interactiva y moderna 💙
    </p>
</div>
""", unsafe_allow_html=True)

# ===== BIENVENIDA =====
st.markdown("""
<div class="card">

<h2>👩‍🍳 Bienvenido a SmartKitchen</h2>

<p>Una cocina inteligente multimodal que permite:</p>

<ul>
<li>🍳 Asistente de Cocina Inteligente</li>
<li>🌡️💧 Monitoreo de Sensores</li>
<li>🌀💨 Control Extractor de Humo</li>
</ul>

</div>
""", unsafe_allow_html=True)

# ===== IMAGEN =====
try:

    img = Image.open("cocina.jpg")

    st.image(
        img,
        caption="💙 Centro de Control SmartKitchen",
        use_container_width=True
    )

except:

    st.image(
        "https://images.unsplash.com/photo-1556911220-e15b29be8c8f",
        caption="💙 Ecosistema SmartKitchen conectado",
        use_container_width=True
    )

# ===== TARJETAS =====
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
    <h3>🤖 IA de Cocina</h3>
    <p>Genera recetas inteligentes.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
    <h3>🌡️ Sensores Inteligentes</h3>
    <p>Monitorea sensores desde Wokwi.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
    <h3>🎀 Experiencia Multimodal</h3>
    <p>Interacción visual y automatización.</p>
    </div>
    """, unsafe_allow_html=True)

# ===== INFO =====
st.info("💙 Usa el menú lateral para navegar.")

# ===== SIDEBAR =====
st.sidebar.title("🍳 SmartKitchen")

st.sidebar.markdown("---")

st.sidebar.success("✨ Navegación")

st.sidebar.markdown("""
- Inicio
- Asistente de Recetas
- Monitor Inteligente
""")

st.sidebar.markdown("---")

st.sidebar.info("💙 Cocina inteligente multimodal")

# ===== FOOTER =====
st.markdown("""
<div class="footer">
SmartKitchen © 2026 💙
</div>
""", unsafe_allow_html=True)
