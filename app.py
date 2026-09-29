"""
👾 Bee's _ Detector de Texto Emocional — 8-Bit Hacker Edition
Interfaz con paleta Verde Neón + Morado Neón, tipografía hacker y estructura invertida.

Requisitos:
    pip install streamlit textblob pandas googletrans==4.0.0-rc1
"""

import streamlit as st
import pandas as pd
from textblob import TextBlob
import re

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Bee's _ Detector de Texto Emocional",
    page_icon="👾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# ESTILOS 8-BIT HACKER & PALETA VERDE/MORADO
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&family=Fira+Code:wght@400;600;700&display=swap');

    /* Fondo Negro Matrix/Arcade con Rejilla 8-bits */
    .stApp {
        background-color: #05030a !important;
        background-image: 
            radial-gradient(#1a0a2a 15%, transparent 16%),
            linear-gradient(to right, rgba(0, 255, 65, 0.05) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(0, 255, 65, 0.05) 1px, transparent 1px) !important;
        background-size: 60px 60px, 20px 20px, 20px 20px !important;
        color: #00ff41 !important;
        font-family: 'Fira Code', monospace !important;
    }

    /* Ocultar barra lateral por defecto para dar aspecto de consola completa */
    [data-testid="stSidebar"] {
        background-color: #0d0614 !important;
        border-right: 4px solid #ff007f !important;
    }
    [data-testid="stSidebar"] * {
        color: #ff007f !important;
        font-family: 'VT323', monospace !important;
        font-size: 1.2rem !important;
    }

    /* Encabezado Principal Hacker / Terminal Header */
    .hacker-header {
        background: #0d0614;
        border: 3px solid #00ff41;
        box-shadow: 6px 6px 0px #ff007f, -6px -6px 0px #00f0ff;
        padding: 15px 25px;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .hacker-title {
        font-family: 'VT323', monospace !important;
        color: #00ff41 !important;
        font-size: 2.8rem;
        letter-spacing: 3px;
        margin: 0;
        text-shadow: 3px 3px 0px #ff007f;
    }

    .hacker-status {
        background: #ff007f;
        color: #000000;
        font-family: 'VT323', monospace;
        font-size: 1.4rem;
        padding: 4px 12px;
        font-weight: bold;
        box-shadow: 3px 3px 0px #00ff41;
    }

    /* Cajas y Contenedores 8-Bits */
    .pixel-box {
        background: #0d0614;
        border: 3px solid #ff007f;
        box-shadow: 5px 5px 0px #00ff41;
        padding: 20px;
        margin-bottom: 25px;
    }

    .pixel-box-green {
        background: #061409;
        border: 3px solid #00ff41;
        box-shadow: 5px 5px 0px #ff007f;
        padding: 20px;
        margin-bottom: 25px;
    }

    .box-title {
        font-family: 'VT323', monospace;
        font-size: 1.8rem;
        color: #00f0ff;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 2px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Terminal de entrada de texto */
    textarea, input[type="text"] {
        background-color: #000000 !important;
        border: 2px solid #00ff41 !important;
        color: #00ff41 !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 1.1rem !important;
        box-shadow: inset 3px 3px 0px #1a0a2a !important;
    }
    textarea:focus, input[type="text"]:focus {
        border-color: #ff007f !important;
        box-shadow: 0px 0px 10px #ff007f !important;
    }

    /* Botón Hacker 8-bits */
    .stButton > button {
        background: #ff007f !important;
        color: #000000 !important;
        border: 3px solid #00ff41 !important;
        font-family: 'VT323', monospace !important;
        font-size: 1.8rem !important;
        letter-spacing: 2px !important;
        padding: 8px 15px !important;
        transition: all 0.1s ease !important;
        width: 100%;
        box-shadow: 4px 4px 0px #00f0ff !important;
        text-transform: uppercase;
    }
    .stButton > button:hover {
        background: #00ff41 !important;
        color: #000000 !important;
        box-shadow: 6px 6px 0px #ff007f !important;
        transform: translate(-2px, -2px);
        cursor: pointer;
    }

    /* Alerta de Resultado en Retro Pixel */
    .retro-alert {
        padding: 15px;
        border: 3px solid;
        font-family: 'VT323', monospace;
        font-size: 1.6rem;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 15px;
    }

    /* Colores Personalizados para Barras */
    .stProgress > div > div > div > div {
        background-color: #ff007f !important;
        box-shadow: 0px 0px 8px #ff007f;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FUNCIONES DE ANÁLISIS NLP
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
        "vuestro", "vuestros", "y", "ya", "yo", "about", "above", "after", "again",
        "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", "been",
        "before", "being", "below", "between", "both", "but", "by", "can", "did", "do",
        "does", "doing", "down", "during", "each", "few", "for", "from", "had", "has",
        "have", "he", "her", "here", "him", "his", "how", "i", "if", "in", "into", "is",
        "it", "its", "me", "more", "most", "my", "no", "not", "of", "off", "on", "once",
        "only", "or", "other", "our", "out", "over", "own", "same", "she", "should", "so",
        "some", "such", "than", "that", "the", "their", "them", "then", "there", "these",
        "they", "this", "those", "through", "to", "too", "under", "until", "up", "very",
        "was", "we", "were", "what", "when", "where", "which", "while", "who", "why", "with", "you"
    ])
    
    palabras = re.findall(r'\b\w+\b', texto.lower())
    palabras_filtradas = [p for p in palabras if p not in stop_words and len(p) > 2]
    
    contador = {}
    for palabra in palabras_filtradas:
        contador[palabra] = contador.get(palabra, 0) + 1
        
    return dict(sorted(contador.items(), key=lambda x: x[1], reverse=True))

def traducir_texto(texto):
    try:
        from googletrans import Translator
        translator = Translator()
        return translator.translate(texto, src='es', dest='en').text
    except Exception:
        return texto

def procesar_texto(texto):
    texto_ingles = traducir_texto(texto)
    blob = TextBlob(texto_ingles)
    
    return {
        "sentimiento": blob.sentiment.polarity,
        "subjetividad": blob.sentiment.subjectivity,
        "contador_palabras": contar_palabras(texto_ingles),
        "texto_original": texto,
        "texto_traducido": texto_ingles
    }

# ─────────────────────────────────────────────
# BANNER PRINCIPAL HACKER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hacker-header">
    <div>
        <h1 class="hacker-title">> Bee's _ Detector de Texto Emocional</h1>
        <span style="color: #ff007f; font-family: 'VT323'; font-size: 1.3rem;">[ROOT@HACK-TERMINAL ~]# SENTIMENT_DECODER_v8.0</span>
    </div>
    <div class="hacker-status">STATUS: ONLINE 🟢</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR RECONFIGURADO
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 👾 MENU DE CONFIGURACIÓN")
    modo = st.radio("SELECCIONAR FUENTE:", ["Entrada Manual", "Cargar Archivo"])
    st.markdown("---")
    st.markdown("### 💾 SISTEMA")
    st.code("CPU: 8-BIT Z80\nRAM: 64KB OK\nNET: CONNECTED", language="text")

# ─────────────────────────────────────────────
# NUEVA ESTRUCTURA INVERTIDA (LAYOUT ARRIBA-ABAJO)
# ─────────────────────────────────────────────

# SECCIÓN 1: ENTRADA DE COMANDOS / TEXTO (ARRIBA)
st.markdown("""
<div class="pixel-box">
    <div class="box-title">> INPUT_TERMINAL (INGRESA TU COMANDO DE TEXTO ABAJO)</div>
""", unsafe_allow_html=True)

if modo == "Entrada Manual":
    texto_input = st.text_area("", height=120, placeholder="> Escribe aquí el texto que deseas hackear / analizar...")
    col_btn, col_blank = st.columns([1, 2])
    with col_btn:
        ejecutar = st.button("⚡ EXECUTE_HACK_SCAN()")
else:
    archivo = st.file_uploader("SELECCIONA ARCHIVO (.TXT / .CSV)", type=["txt", "csv", "md"])
    if archivo is not None:
        texto_input = archivo.getvalue().decode("utf-8")
        ejecutar = st.button("⚡ DECODE_FILE()")
    else:
        texto_input = ""
        ejecutar = False

st.markdown("</div>", unsafe_allow_html=True)

# SECCIÓN 2: RESULTADOS PRINCIPALES DE LA TELEMETRÍA (CENTRO)
if ejecutar and texto_input.strip():
    with st.spinner("DECODIFICANDO MATRIZ EMOCIONAL..."):
        res = procesar_texto(texto_input)

    st.markdown("""
    <div class="pixel-box-green">
        <div class="box-title" style="color: #00ff41;">> DECODED_OUTPUT (DIAGNÓSTICO OBTENIDO)</div>
    """, unsafe_allow_html=True)

    # ALERTA DE DIAGNÓSTICO RETRO
    if res["sentimiento"] > 0.05:
        msg = "VALOR: POSITIVO // VIBRA DETECTADA: OPTIMISTA / BUENA ENERGÍA"
        border_c = "#00ff41"
        bg_c = "#06240d"
        icon = "👾"
    elif res["sentimiento"] < -0.05:
        msg = "VALOR: NEGATIVO // VIBRA DETECTADA: HOSTIL / CRÍTICA"
        border_c = "#ff007f"
        bg_c = "#290416"
        icon = "💀"
    else:
        msg = "VALOR: NEUTRAL // VIBRA DETECTADA: ESTABLE / SIN SESGO"
        border_c = "#00f0ff"
        bg_c = "#042029"
        icon = "🤖"

    st.markdown(f"""
    <div class="retro-alert" style="border-color: {border_c}; background-color: {bg_c}; color: {border_c};">
        <div style="font-size: 2.5rem;">{icon}</div>
        <div>
            <div>[RESULTADO DE LA MATRIZ]</div>
            <div style="font-weight: bold;">{msg}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # METRICAS EN TRES COLUMNAS
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.markdown("<b style='color:#00f0ff;'>POLARIDAD:</b>", unsafe_allow_html=True)
        st.progress((res["sentimiento"] + 1) / 2)
        st.code(f"VALOR: {res['sentimiento']:.2f}")

    with m_col2:
        st.markdown("<b style='color:#ff007f;'>SUBJETIVIDAD:</b>", unsafe_allow_html=True)
        st.progress(res["subjetividad"])
        st.code(f"VALOR: {res['subjetividad']:.2f}")

    with m_col3:
        st.markdown("<b style='color:#00ff41;'>PALABRAS CLAVE:</b>", unsafe_allow_html=True)
        st.code(f"TOTAL: {len(res['contador_palabras'])} palabras")

    st.markdown("</div>", unsafe_allow_html=True)

    # SECCIÓN 3: PANELES SECUNDARIOS EN PARALELO (ABAJO)
    c_left, c_right = st.columns(2)

    with c_left:
        st.markdown("""
        <div class="pixel-box">
            <div class="box-title">> TOP_KEYWORDS_FREQUENCIES</div>
        """, unsafe_allow_html=True)
        if res["contador_palabras"]:
            top_words = dict(list(res["contador_palabras"].items())[:7])
            st.bar_chart(top_words)
        else:
            st.write("No hay palabras suficientes para graficar.")
        st.markdown("</div>", unsafe_allow_html=True)

    with c_right:
        st.markdown("""
        <div class="pixel-box">
            <div class="box-title">> TRADUCCIÓN_RAW (ENGLISH)</div>
        """, unsafe_allow_html=True)
        st.code(res["texto_traducido"], language="text")
        st.markdown("</div>", unsafe_allow_html=True)

elif ejecutar:
    st.warning("> ERROR: Debes ingresar un texto válido para iniciar el escaneo.")
