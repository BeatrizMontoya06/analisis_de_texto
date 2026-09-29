"""
⚙️ Bee's _ Detector de Texto Emocional
Aplicación Streamlit con interfaz metálica, neón verde y estética futurista Y2K.

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
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# ESTILOS METÁLICOS / FUTURISTAS RETRO
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;600;700&display=swap');

    /* Fondo Degradado Metálico Oscuro */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #152417 0%, #090f0a 60%, #020503 100%) !important;
        background-attachment: fixed !important;
        color: #e0e0e0 !important;
        font-family: 'Rajdhani', sans-serif !important;
    }

    /* Sidebar - Panel Lateral de Control Metálico */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1c261e 0%, #0d140e 50%, #050805 100%) !important;
        border-right: 2px solid #00ff66 !important;
        box-shadow: 8px 0px 20px rgba(0, 255, 102, 0.15);
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
        font-family: 'Rajdhani', sans-serif !important;
    }

    /* Header Metálico / HUD Cyber */
    .cyber-header {
        background: linear-gradient(180deg, #2a3d2d 0%, #111a12 100%);
        border: 2px solid #00ff66;
        border-radius: 6px;
        padding: 20px 25px;
        margin-bottom: 25px;
        box-shadow: 0px 0px 20px rgba(0, 255, 102, 0.3), inset 0px 1px 0px rgba(255, 255, 255, 0.2);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .cyber-title {
        font-family: 'Orbitron', sans-serif !important;
        color: #ffffff !important;
        font-size: 2.1rem;
        font-weight: 900;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 0;
        text-shadow: 0px 0px 12px #00ff66;
    }

    .cyber-badge {
        background: linear-gradient(180deg, #00ff66 0%, #009933 100%);
        color: #000000;
        padding: 6px 14px;
        font-weight: bold;
        font-family: 'Orbitron', sans-serif;
        border-radius: 4px;
        font-size: 0.85rem;
        letter-spacing: 1px;
        box-shadow: 0px 0px 10px #00ff66;
    }

    /* Modulos / Tarjetas con Bisel Metálico */
    .cyber-card {
        background: linear-gradient(135deg, rgba(25, 36, 27, 0.9) 0%, rgba(10, 15, 11, 0.95) 100%);
        border: 1px solid #00ff66;
        border-top: 3px solid #00ff66;
        border-radius: 6px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(4px);
    }

    .card-title {
        font-family: 'Orbitron', sans-serif;
        color: #00ff66;
        font-size: 1.2rem;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        display: flex;
        align-items: center;
        gap: 10px;
        text-shadow: 0px 0px 8px rgba(0, 255, 102, 0.5);
    }

    /* Entrada de Texto Terminal */
    textarea, input[type="text"] {
        background-color: #060a07 !important;
        border: 2px solid #1e4d2b !important;
        border-radius: 4px !important;
        color: #00ff66 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1.15rem !important;
        font-weight: 600 !important;
    }
    textarea:focus, input[type="text"]:focus {
        border-color: #00ff66 !important;
        box-shadow: 0px 0px 12px rgba(0, 255, 102, 0.6) !important;
    }

    /* Botones de Comando Neón */
    .stButton > button {
        background: linear-gradient(180deg, #1c4d28 0%, #0a2612 100%) !important;
        color: #ffffff !important;
        border: 2px solid #00ff66 !important;
        border-radius: 4px !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        padding: 12px 20px !important;
        transition: all 0.2s ease !important;
        width: 100%;
        box-shadow: 0px 0px 12px rgba(0, 255, 102, 0.3) !important;
    }
    .stButton > button:hover {
        background: #00ff66 !important;
        color: #000000 !important;
        box-shadow: 0px 0px 25px #00ff66 !important;
        cursor: pointer;
    }

    /* Módulo de Alerta de Diagnóstico */
    .status-box {
        background: linear-gradient(90deg, #122917 0%, #08120a 100%);
        border: 2px solid #00ff66;
        border-radius: 6px;
        padding: 16px;
        display: flex;
        align-items: center;
        gap: 15px;
        box-shadow: 0px 0px 15px rgba(0, 255, 102, 0.3);
        margin-top: 15px;
    }

    /* Barra de Progreso Personalizada */
    .stProgress > div > div > div > div {
        background-color: #00ff66 !important;
        box-shadow: 0px 0px 10px #00ff66;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FUNCIONES DE ANÁLISIS
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
# ENCABEZADO
# ─────────────────────────────────────────────
st.markdown("""
<div class="cyber-header">
    <div>
        <h1 class="cyber-title">Bee's _ Detector de Texto Emocional</h1>
        <span style="color: #00ff66; font-size: 0.9rem; letter-spacing: 1px;">SYSTEM HUD // ANALIZADOR DE TELEMETRÍA TEXTUAL</span>
    </div>
    <div class="cyber-badge">SYSTEM ONLINE</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PANEL LATERAL
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ PANEL DE CONTROL")
    st.markdown("""
    <div style="background: rgba(0,0,0,0.6); padding: 12px; border-left: 3px solid #00ff66; border-radius: 4px;">
        <b style="color:#00ff66;">Núcleo:</b> Matrix-2000<br>
        <b style="color:#00ff66;">Frecuencia:</b> 60 Hz<br>
        <b>Estado:</b> Procesando señales... 🟢
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📥 MODO DE INGRESO")
    modo = st.selectbox(
        "Seleccionar fuente:",
        ["Entrada Directa", "Archivo de Texto"]
    )
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.85rem; color: #88aa8f; font-family: 'Orbitron';">
        > READY FOR DATA INPUT<br>
        > WAITING FOR USER SIGNAL...
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CUERPO PRINCIPAL
# ─────────────────────────────────────────────
col_main, col_info = st.columns([2.5, 1])

with col_main:
    st.markdown("""
    <div class="cyber-card">
        <div class="card-title">📡 Terminal de Entrada de Texto</div>
    """, unsafe_allow_html=True)

    if modo == "Entrada Directa":
        texto = st.text_area("", height=160, placeholder="Escribe o pega aquí el texto para analizar...")
        if st.button("EXECUTE SCAN // INICIAR ESCANEO"):
            if texto.strip():
                with st.spinner("Procesando espectro emocional..."):
                    res = procesar_texto(texto)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("<div class='card-title'>📊 RESULTADO DE LA TELEMETRÍA</div>", unsafe_allow_html=True)
                    
                    if res["sentimiento"] > 0.05:
                        diag = "SENTIMIENTO POSITIVO // VIBRAS OPTIMISTAS DETECTADAS"
                        icon = "🟢"
                        c_border = "#00ff66"
                    elif res["sentimiento"] < -0.05:
                        diag = "SENTIMIENTO NEGATIVO // TENSION / CRITICIDAD DETECTADA"
                        icon = "🔴"
                        c_border = "#ff3355"
                    else:
                        diag = "SENTIMIENTO NEUTRAL // ESTADO ESTABLE / EQUILIBRADO"
                        icon = "🟡"
                        c_border = "#ffff00"

                    st.markdown(f"""
                    <div class="status-box" style="border-color: {c_border};">
                        <div style="font-size: 2rem;">{icon}</div>
                        <div>
                            <div style="color: #ffffff; font-family: 'Orbitron'; font-size: 0.85rem;">DIAGNÓSTICO FINAL</div>
                            <div style="color: {c_border}; font-weight: bold; font-size: 1.1rem; font-family: 'Orbitron';">{diag}</div>
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

                    # Frecuencia
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.write("**Términos Más Frecuentes:**")
                    if res["contador_palabras"]:
                        top_p = dict(list(res["contador_palabras"].items())[:8])
                        st.bar_chart(top_p)

            else:
                st.warning("Escribe algún comando o texto antes de presionar escanear.")

    elif modo == "Archivo de Texto":
        archivo = st.file_uploader("Cargar documento de datos (.txt, .md, .csv)", type=["txt", "csv", "md"])
        if archivo is not None:
            contenido = archivo.getvalue().decode("utf-8")
            if st.button("ANALYZING FILE DATA"):
                with st.spinner("Decodificando archivo..."):
                    res = procesar_texto(contenido)
                    st.success("¡Datos procesados con éxito!")
                    st.write(f"Polaridad General: `{res['sentimiento']:.2f}`")
                    st.write(f"Subjetividad General: `{res['subjetividad']:.2f}`")

    st.markdown("</div>", unsafe_allow_html=True)

with col_info:
    st.markdown("""
    <div class="cyber-card">
        <div class="card-title">🔍 ESPECIFICACIONES</div>
        <p style="font-size: 0.9rem; color: #a3c2a0;">
            <b>Módulo NLP:</b> TextBlob Engine<br>
            <b>Traducción:</b> Google Translate API<br>
            <b>Interfaz:</b> Metal Cyber HUD
        </p>
    </div>
    
    <div class="cyber-card">
        <div class="card-title">🛡️ ESTADO DE RED</div>
        <p style="font-size: 0.85rem; color: #00ff66;">
            [OK] CONEXIÓN SEGURA<br>
            [OK] MOTOR DE BÚSQUEDA LISTO<br>
            [OK] MEMORIA BUFFER VACIADA
        </p>
    </div>
    """, unsafe_allow_html=True)
