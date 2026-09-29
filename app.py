"""
🎮 Bee's _ Detector de Texto Emocional — Xbox 360 Dashboard Style
Aplicación Streamlit inspirada en la interfaz clásica NXE de Xbox 360.

Requisitos:
    pip install streamlit textblob pandas googletrans==4.0.0-rc1
"""

import streamlit as st
import pandas as pd
from textblob import TextBlob
import re

# ─────────────────────────────────────────────
# CONFIGURACIÓN PÁGINA XBOX 360
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Bee's _ Detector de Texto Emocional",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# ESTILOS XBOX 360 DASHBOARD (GREEN NEON / DARK HUD)
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;600;700&display=swap');

    /* Fondo Degradado Xbox 360 Dashboard */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #1e3919 0%, #0d130c 50%, #050805 100%) !important;
        background-attachment: fixed !important;
        color: #e6e6e6 !important;
        font-family: 'Rajdhani', sans-serif !important;
    }

    /* Sidebar - Menú Guía Xbox */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #107c41 0%, #0a3d20 40%, #051a0d 100%) !important;
        border-right: 3px solid #9bf00b !important;
        box-shadow: 10px 0px 25px rgba(155, 240, 11, 0.2);
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
        font-family: 'Rajdhani', sans-serif !important;
    }

    /* Encabezado Xbox / Gamer Tag Header */
    .xbox-header {
        background: linear-gradient(90deg, #107c41 0%, #1e592f 50%, #000000 100%);
        border-left: 8px solid #9bf00b;
        border-bottom: 2px solid #9bf00b;
        padding: 18px 25px;
        border-radius: 4px;
        margin-bottom: 25px;
        box-shadow: 0px 4px 15px rgba(16, 124, 65, 0.6);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .xbox-title {
        font-family: 'Orbitron', sans-serif !important;
        color: #ffffff !important;
        font-size: 2rem;
        font-weight: 900;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 0;
        text-shadow: 0px 0px 10px #9bf00b;
    }

    .xbox-badge {
        background: #9bf00b;
        color: #000000;
        padding: 4px 12px;
        font-weight: bold;
        font-family: 'Orbitron', sans-serif;
        border-radius: 3px;
        font-size: 0.85rem;
    }

    /* Tarjetas de Interfaz / Blades estilo Xbox */
    .xbox-blade {
        background: rgba(20, 25, 22, 0.85);
        border: 1px solid #107c41;
        border-top: 4px solid #9bf00b;
        border-radius: 6px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(5px);
    }

    .blade-title {
        font-family: 'Orbitron', sans-serif;
        color: #9bf00b;
        font-size: 1.2rem;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Estilo de Cajas de Texto e Inputs */
    textarea, input[type="text"] {
        background-color: #0d130c !important;
        border: 2px solid #107c41 !important;
        border-radius: 4px !important;
        color: #9bf00b !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    textarea:focus, input[type="text"]:focus {
        border-color: #9bf00b !important;
        box-shadow: 0px 0px 10px rgba(155, 240, 11, 0.5) !important;
    }

    /* Botones de Mando Xbox (A Button Glow) */
    .stButton > button {
        background: linear-gradient(180deg, #107c41 0%, #0b4f29 100%) !important;
        color: #ffffff !important;
        border: 2px solid #9bf00b !important;
        border-radius: 4px !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
        width: 100%;
        box-shadow: 0px 0px 10px rgba(16, 124, 65, 0.4) !important;
    }
    .stButton > button:hover {
        background: #9bf00b !important;
        color: #000000 !important;
        box-shadow: 0px 0px 20px #9bf00b !important;
        cursor: pointer;
    }

    /* Indicador de Logro / Gamercard Result */
    .achievement-unlocked {
        background: linear-gradient(90deg, #107c41 0%, #18281a 100%);
        border: 2px solid #9bf00b;
        border-radius: 5px;
        padding: 15px;
        display: flex;
        align-items: center;
        gap: 15px;
        box-shadow: 0px 0px 15px rgba(155, 240, 11, 0.4);
        margin-top: 15px;
    }

    /* Custom Progress Bar Xbox Green */
    .stProgress > div > div > div > div {
        background-color: #9bf00b !important;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FUNCIONES DE PROCESAMIENTO
# ─────────────────────────────────────────────

def contar_palabras(texto):
    stop_words = set([
        "a", "al", "algo", "algunas", "algunos", "ante", "antes", "como", "con", "contra",
        "cual", "cuando", "de", "del", "desde", "donde", "durante", "e", "el", "ella",
        "ellas", "ellos", "en", "entre", "era", "eras", "es", "esa", "esas", "ese",
        "eso", "esos", "esta", "estas", "este", "esto", "estos", "ha", "había", "han",
        "has", "hasta", "he", "la", "las", "le", "les", "lo", "los", "me", "mi", "mía",
        "mías", "mío", "míos", "mis", "mucho", "muchos", "muy", "nada", "ni", "no", "nos",
        "nosotras", "nosotros", "nuestra", "nuestras", "nuestro", "nuestros", "o", "os", 
        "otra", "otras", "otro", "otros", "para", "pero", "poco", "por", "porque", "que", 
        "quien", "quienes", "qué", "se", "sea", "sean", "según", "si", "sido", "sin", 
        "sobre", "sois", "somos", "son", "soy", "su", "sus", "suya", "suyas", "suyo", 
        "suyos", "también", "tanto", "te", "tenéis", "tenemos", "tener", "tengo", "ti", 
        "tiene", "tienen", "todo", "todos", "tu", "tus", "tuya", "tuyas", "tuyo", "tuyos", 
        "tú", "un", "una", "uno", "unos", "vosotras", "vosotros", "vuestra", "vuestras", 
        "vuestro", "vuestros", "y", "ya", "yo", "a", "about", "above", "after", "again",
        "against", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", 
        "been", "before", "being", "below", "between", "both", "but", "by", "can", "could", 
        "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", 
        "had", "has", "have", "he", "her", "here", "him", "his", "how", "i", "if", "in", 
        "into", "is", "it", "its", "me", "more", "most", "my", "no", "not", "of", "off", 
        "on", "once", "only", "or", "other", "our", "out", "over", "own", "same", "she", 
        "should", "so", "some", "such", "than", "that", "the", "their", "them", "then", 
        "there", "these", "they", "this", "those", "through", "to", "too", "under", 
        "until", "up", "very", "was", "we", "were", "what", "when", "where", "which", 
        "while", "who", "whom", "why", "with", "would", "you", "your"
    ])
    
    palabras = re.findall(r'\b\w+\b', texto.lower())
    palabras_filtradas = [p for p in palabras if p not in stop_words and len(p) > 2]
    
    contador = {}
    for palabra in palabras_filtradas:
        contador[palabra] = contador.get(palabra, 0) + 1
        
    return dict(sorted(contador.items(), key=lambda x: x[1], reverse=True)), palabras_filtradas

def traducir_texto(texto):
    try:
        from googletrans import Translator
        translator = Translator()
        return translator.translate(texto, src='es', dest='en').text
    except Exception:
        return texto

def procesar_texto(texto):
    texto_original = texto
    texto_ingles = traducir_texto(texto)
    blob = TextBlob(texto_ingles)
    
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    
    frases_orig = [f.strip() for f in re.split(r'[.!?]+', texto_original) if f.strip()]
    frases_trad = [f.strip() for f in re.split(r'[.!?]+', texto_ingles) if f.strip()]
    
    frases_comb = []
    for i in range(min(len(frases_orig), len(frases_trad))):
        frases_comb.append({
            "original": frases_orig[i],
            "traducido": frases_trad[i]
        })
        
    contador, palabras = contar_palabras(texto_ingles)
    
    return {
        "sentimiento": sentimiento,
        "subjetividad": subjetividad,
        "frases": frases_comb,
        "contador_palabras": contador,
        "texto_original": texto_original,
        "texto_traducido": texto_ingles
    }

# ─────────────────────────────────────────────
# HEADER DASHBOARD
# ─────────────────────────────────────────────
st.markdown("""
<div class="xbox-header">
    <div>
        <h1 class="xbox-title">Bee's _ Detector de Texto Emocional</h1>
        <span style="color: #a3c2a0; font-size: 0.95rem;">SYSTEM DASHBOARD // SENTIMENT DECODING HUD</span>
    </div>
    <div class="xbox-badge">XBOX LIVE 360</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR / GUÍA XBOX
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎮 GAMER CARD")
    st.markdown("""
    <div style="background: rgba(0,0,0,0.5); padding: 12px; border-left: 4px solid #9bf00b; border-radius: 4px;">
        <b style="color:#9bf00b;">Gamertag:</b> Bee_Master_360<br>
        <b style="color:#9bf00b;">GamerScore:</b> 25,400 G<br>
        <b>Estado:</b> En línea en Xbox Live 🟢
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🕹️ MODO DE ENTRADA")
    modo = st.selectbox(
        "Selecciona fuente de datos:",
        ["Entrada Directa", "Archivo de Texto"]
    )
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.85rem; color: #a3c2a0;">
        <b>[A] Seleccionar</b><br>
        <b>[B] Atrás</b><br>
        <b>[X] Escanear Texto</b>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PANEL PRINCIPAL
# ─────────────────────────────────────────────
col_left, col_right = st.columns([2.5, 1])

with col_left:
    st.markdown("""
    <div class="xbox-blade">
        <div class="blade-title">📡 Entrada de Señal de Texto</div>
    """, unsafe_allow_html=True)

    if modo == "Entrada Directa":
        texto = st.text_area("", height=160, placeholder="Escribe el comando o frase a escanear...")
        if st.button("PRESS [A] TO ANALYZE // INICIAR ESCANEO"):
            if texto.strip():
                with st.spinner("Procesando telemetría emocional..."):
                    res = procesar_texto(texto)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("<div class='blade-title'>🏆 RESULTADO DEL DIAGNÓSTICO</div>", unsafe_allow_html=True)
                    
                    # LOGRO DESBLOQUEADO
                    if res["sentimiento"] > 0.05:
                        msg = "¡LOGRO DESBLOQUEADO! (50G) — Sentimiento Positivo / High Vibes Detectadas"
                        color_border = "#9bf00b"
                    elif res["sentimiento"] < -0.05:
                        msg = "¡LOGRO DESBLOQUEADO! (20G) — Sentimiento Negativo / Dark Mood Detectado"
                        color_border = "#ff3333"
                    else:
                        msg = "¡LOGRO DESBLOQUEADO! (10G) — Sentimiento Neutral / Estado Estable"
                        color_border = "#ffff00"

                    st.markdown(f"""
                    <div class="achievement-unlocked" style="border-color: {color_border};">
                        <div style="font-size: 2.2rem;">🏆</div>
                        <div>
                            <div style="color: #ffffff; font-family: 'Orbitron'; font-size: 0.9rem; text-transform: uppercase;">Misión Completada</div>
                            <div style="color: #9bf00b; font-weight: bold; font-size: 1.1rem;">{msg}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    m1, m2 = st.columns(2)
                    with m1:
                        st.write("**Polaridad (-1.0 a 1.0):**")
                        st.progress((res["sentimiento"] + 1) / 2)
                        st.write(f"Valor: `{res['sentimiento']:.2f}`")
                    with m2:
                        st.write("**Subjetividad (0.0 a 1.0):**")
                        st.progress(res["subjetividad"])
                        st.write(f"Valor: `{res['subjetividad']:.2f}`")

                    # Frecuencia de palabras
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.write("**Top Palabras Más Usadas:**")
                    if res["contador_palabras"]:
                        top_p = dict(list(res["contador_palabras"].items())[:8])
                        st.bar_chart(top_p)

            else:
                st.warning("Por favor ingresa texto en la consola.")

    elif modo == "Archivo de Texto":
        archivo = st.file_uploader("Cargar archivo (.txt, .md, .csv)", type=["txt", "csv", "md"])
        if archivo is not None:
            contenido = archivo.getvalue().decode("utf-8")
            if st.button("PRESS [A] TO SCAN FILE"):
                with st.spinner("Analizando archivo de datos..."):
                    res = procesar_texto(contenido)
                    st.success("¡Archivo analizado con éxito!")
                    st.write(f"Polaridad General: `{res['sentimiento']:.2f}`")
                    st.write(f"Subjetividad General: `{res['subjetividad']:.2f}`")

    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div class="xbox-blade">
        <div class="blade-title">⚙️ SYSTEM INFO</div>
        <p style="font-size: 0.9rem; color: #a3c2a0;">
            <b>Motor:</b> TextBlob NLP v2.0<br>
            <b>Consola:</b> Bee's Dashboard<br>
            <b>Traducción:</b> Google Translation Engine
        </p>
    </div>
    
    <div class="xbox-blade">
        <div class="blade-title">🟢 AMIGOS EN LÍNEA</div>
        <ul style="padding-left: 15px; font-size: 0.9rem;">
            <li>MasterChief_117 (Jugando Halo 3)</li>
            <li>Marcus_Fenix (Gears of War)</li>
            <li>Cortana_AI (En el menú)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
