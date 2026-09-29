"""
🐝 Bee Emo-tional — The Y2K Text & Sentiment Analyzer Blog
Aplicación Streamlit estilo Blog de los 2000s para análisis completo de texto.

Dependencias principales:
    pip install streamlit textblob pandas googletrans==4.0.0-rc1
"""

import streamlit as st
import pandas as pd
from textblob import TextBlob
import re

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA Y2K
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="★~ Bee Emo-tional ~★ Text Diary Analyzer",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# ESTILOS RETRO BLOG (AÑOS 2000 / MYSPACE / BLOGGER)
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:ital,wght@0,700;1,400&family=Press+Start+2P&display=swap');

    /* Fondo degradado estilo Web 2.0 / Y2K */
    .stApp {
        background: linear-gradient(135deg, #ff99dd 0%, #ffcc00 25%, #66ffff 50%, #ff66cc 75%, #cc66ff 100%) !important;
        background-attachment: fixed !important;
        font-family: 'Comic Sans MS', 'Comic Neue', cursive, sans-serif !important;
    }

    /* Sidebar estilo Perfil de Myspace / MSN */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ff007f 0%, #4b0082 100%) !important;
        border-right: 4px dashed #ffff00 !important;
        box-shadow: 5px 0px 15px rgba(0,0,0,0.3);
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
        font-family: 'Comic Sans MS', cursive !important;
    }

    /* Header del Blog */
    .blog-header {
        background: #ffff00;
        border: 4px solid #ff007f;
        box-shadow: 8px 8px 0px #00ffff, 16px 16px 0px #ff007f;
        padding: 20px;
        text-align: center;
        margin-bottom: 25px;
        border-radius: 15px;
    }
    
    .blog-title {
        font-family: 'Press Start 2P', 'Comic Sans MS', cursive !important;
        color: #ff007f !important;
        text-shadow: 3px 3px 0px #00ffff, 6px 6px 0px #000000;
        font-size: 2.2rem;
        margin: 0;
    }

    .blog-subtitle {
        color: #7928ca;
        font-weight: bold;
        font-size: 1.1rem;
        margin-top: 10px;
    }

    /* Contenedores estilo Entrada de Blog / Posts */
    .blog-post {
        background: #ffffff;
        border: 4px solid #000000;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 8px 8px 0px #ff007f;
    }

    .post-header {
        background: #00ffff;
        padding: 10px 15px;
        border-radius: 10px;
        border: 2px solid #000000;
        font-weight: bold;
        color: #000000;
        margin-bottom: 15px;
    }

    /* Botones personalizados estilo Neón */
    .stButton > button {
        background: linear-gradient(180deg, #ff007f 0%, #ff66cc 100%) !important;
        color: #ffffff !important;
        border: 3px solid #000000 !important;
        border-radius: 15px !important;
        font-family: 'Comic Sans MS', cursive !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        box-shadow: 4px 4px 0px #000000 !important;
        text-shadow: 1px 1px 0px #000 !important;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translate(-2px, -2px) !important;
        box-shadow: 6px 6px 0px #00ffff !important;
    }

    /* Cajas de texto e inputs */
    textarea, input[type="text"] {
        background-color: #ffffcc !important;
        border: 3px solid #ff007f !important;
        border-radius: 10px !important;
        color: #000000 !important;
        font-family: 'Comic Sans MS', cursive !important;
    }

    /* Modificación de Expanders */
    .streamlit-expanderHeader {
        background-color: #ffcc00 !important;
        border: 2px solid #000 !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FUNCIONES DE PROCESAMIENTO DE TEXTO
# ─────────────────────────────────────────────

def contar_palabras(texto):
    """Filtra palabras vacías y obtiene la frecuencia de términos."""
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
        "vuestro", "vuestros", "y", "ya", "yo",
        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", 
        "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", 
        "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", 
        "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", 
        "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", 
        "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", 
        "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", 
        "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", 
        "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", 
        "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", 
        "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", 
        "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", 
        "the", "their", "theirs", "them", "themselves", "then", "there", "there's", 
        "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", 
        "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", 
        "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", 
        "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", 
        "why's", "with", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've",
        "your", "yours", "yourself", "yourselves"
    ])
    
    palabras = re.findall(r'\b\w+\b', texto.lower())
    palabras_filtradas = [p for p in palabras if p not in stop_words and len(p) > 2]
    
    contador = {}
    for palabra in palabras_filtradas:
        contador[palabra] = contador.get(palabra, 0) + 1
        
    contador_ordenado = dict(sorted(contador.items(), key=lambda x: x[1], reverse=True))
    return contador_ordenado, palabras_filtradas

def traducir_texto(texto):
    """Manejo de traducción al inglés con fallback en caso de fallar."""
    try:
        from googletrans import Translator
        translator = Translator()
        traduccion = translator.translate(texto, src='es', dest='en')
        return traduccion.text
    except Exception as e:
        return texto

def procesar_texto(texto):
    """Ejecuta el pipeline completo de análisis."""
    texto_original = texto
    texto_ingles = traducir_texto(texto)
    blob = TextBlob(texto_ingles)
    
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    
    frases_originales = [f.strip() for f in re.split(r'[.!?]+', texto_original) if f.strip()]
    frases_traducidas = [f.strip() for f in re.split(r'[.!?]+', texto_ingles) if f.strip()]
    
    frases_combinadas = []
    for i in range(min(len(frases_originales), len(frases_traducidas))):
        frases_combinadas.append({
            "original": frases_originales[i],
            "traducido": frases_traducidas[i]
        })
        
    contador_palabras, palabras = contar_palabras(texto_ingles)
    
    return {
        "sentimiento": sentimiento,
        "subjetividad": subjetividad,
        "frases": frases_combinadas,
        "contador_palabras": contador_palabras,
        "palabras": palabras,
        "texto_original": texto_original,
        "texto_traducido": texto_ingles
    }

# ─────────────────────────────────────────────
# VISUALIZACIÓN DE RESULTADOS RETRO
# ─────────────────────────────────────────────
def crear_visualizaciones(resultados):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🖤 Mood & Sentimiento")
        
        sentimiento_norm = (resultados["sentimiento"] + 1) / 2
        st.write("**Polaridad Emo-cional:**")
        st.progress(sentimiento_norm)
        
        if resultados["sentimiento"] > 0.05:
            st.success(f"📈 Positivo / Cheerful vibes ({resultados['sentimiento']:.2f}) 😊")
        elif resultados["sentimiento"] < -0.05:
            st.error(f"📉 Negativo / Pure Emo Mood ({resultados['sentimiento']:.2f}) 😔")
        else:
            st.info(f"📊 Neutral / Balanced Vibe ({resultados['sentimiento']:.2f}) 😐")
            
        st.write("**Subjetividad:**")
        st.progress(resultados["subjetividad"])
        
        if resultados["subjetividad"] > 0.5:
            st.warning(f"💭 Alta subjetividad / Muy personal ({resultados['subjetividad']:.2f})")
        else:
            st.info(f"📋 Baja subjetividad / Basado en datos ({resultados['subjetividad']:.2f})")

    with col2:
        st.subheader("📊 Palabras Frecuentes (Top 10)")
        if resultados["contador_palabras"]:
            palabras_top = dict(list(resultados["contador_palabras"].items())[:10])
            st.bar_chart(palabras_top)

    st.markdown("---")
    st.subheader("🌐 Traducción al Inglés")
    with st.expander("Ver diario traducido completo"):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Original (Español):**")
            st.text(resultados["texto_original"])
        with c2:
            st.markdown("**Traducción (Inglés):**")
            st.text(resultados["texto_traducido"])
            
    st.markdown("---")
    st.subheader("✂️ Frases Detectadas & Análisis Individual")
    if resultados["frases"]:
        for i, frase_dict in enumerate(resultados["frases"][:10], 1):
            frase_original = frase_dict["original"]
            frase_traducida = frase_dict["traducido"]
            
            try:
                blob_frase = TextBlob(frase_traducida)
                sentimiento = blob_frase.sentiment.polarity
                
                if sentimiento > 0.05:
                    emoji = "😊"
                elif sentimiento < -0.05:
                    emoji = "🖤"
                else:
                    emoji = "☁️"
                    
                st.markdown(f"**{i}. {emoji} Original:** *\"{frase_original}\"*")
                st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;**Traducido:** *\"{frase_traducida}\"* `(Score: {sentimiento:.2f})`")
                st.markdown("<hr style='border:1px dashed #ccc;'>", unsafe_allow_html=True)
            except:
                st.write(f"{i}. **Original:** *\"{frase_original}\"*")

# ─────────────────────────────────────────────
# HEADER & SIDEBAR Y2K
# ─────────────────────────────────────────────
st.markdown("""
<div class="blog-header">
    <h1 class="blog-title">★~ Bee Emo-tional ~★</h1>
    <p class="blog-subtitle">✨ Text & Diary Analyzer Blog Spot ~ Myspace Edition ✨</p>
    <marquee style="color:#ff007f; font-weight:bold; margin-top:5px;">
        🐝 Bienvenido a Bee Emo-tional 🐝 :: Analiza tus textos, diarios y canciones :: Listen to My Chemical Romance & Write!
    </marquee>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🐝 Blogger Profile")
    st.markdown("<b>User:</b> Bee_Emo_Queen<br><b>Status:</b> Online on MSN 🟢<br><b>Current Mood:</b> Analyzing Words... 🎧", unsafe_allow_html=True)
    st.markdown("---")
    st.title("⚙️ Menú de Entradas")
    modo = st.selectbox(
        "Selecciona el modo de entrada:",
        ["Texto directo", "Archivo de texto"]
    )
    st.markdown("---")
    st.markdown("<b>Music Playing:</b><br>🎵 *I'm Not Okay (I Promise)*", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CUERPO PRINCIPAL (POST DE BLOG)
# ─────────────────────────────────────────────
col_main, col_blogroll = st.columns([3, 1])

with col_main:
    st.markdown("""
    <div class="blog-post">
        <div class="post-header">
            📝 POSTED BY Bee_Emo_Queen | 🕒 CATEGORY: TEXT ANALYZER 2000s
        </div>
    """, unsafe_allow_html=True)

    if modo == "Texto directo":
        st.subheader("✍️ Ingresa tu texto o entrada de diario")
        texto = st.text_area("", height=180, placeholder="Escribe o pega aquí la letra de una canción, un diario o una frase...")
        
        if st.button("🔮 ANALIZAR VIBRAS Y TEXTO"):
            if texto.strip():
                with st.spinner("🤖 Leyendo tus secretos y calculando palabras..."):
                    resultados = procesar_texto(texto)
                    crear_visualizaciones(resultados)
            else:
                st.warning("Escribe algo antes de presionar el botón ~ ★")

    elif modo == "Archivo de texto":
        st.subheader("📁 Sube tu archivo de texto (.txt, .md, .csv)")
        archivo = st.file_uploader("", type=["txt", "csv", "md"])
        
        if archivo is not None:
            try:
                contenido = archivo.getvalue().decode("utf-8")
                with st.expander("📄 Vista previa del archivo"):
                    st.text(contenido[:1000] + ("..." if len(contenido) > 1000 else ""))
                
                if st.button("🔮 ANALIZAR ARCHIVO"):
                    with st.spinner("🤖 Leyendo archivo completo..."):
                        resultados = procesar_texto(contenido)
                        crear_visualizaciones(resultados)
            except Exception as e:
                st.error(f"Error al leer el archivo: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

with col_blogroll:
    st.markdown("""
    <div class="blog-post" style="padding:15px;">
        <h4 style="margin-top:0; color:#ff007f; border-bottom:2px solid #000;">💖 Blogroll</h4>
        <ul style="padding-left:15px; font-size:0.9rem;">
            <li>xX_EmoBoy_2006_Xx</li>
            <li>Glitter_Girl_Y2K</li>
            <li>Punk_Rocker_99</li>
        </ul>
    </div>
    
    <div class="blog-post" style="padding:15px;">
        <h4 style="margin-top:0; color:#7928ca; border-bottom:2px solid #000;">📚 Info del Análisis</h4>
        <p style="font-size:0.85rem;">Este blog analiza el texto traduciéndolo al inglés para usar el léxico de TextBlob, extrayendo polaridad, subjetividad y conteo de palabras clave sin librerías pesadas.</p>
    </div>
    """, unsafe_allow_html=True)

# Pie de página retro
st.markdown("---")
st.markdown("<p style='text-align: center; color: #000;'>★~ Bee Emo-tional Blog Spot — Hecho con Streamlit & TextBlob ~★</p>", unsafe_allow_html=True)
