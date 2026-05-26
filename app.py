# =========================================================
# GUARDIAN VISION - INTEGRADO CON TEACHABLE MACHINE + WOKWI
# =========================================================
 
import streamlit as st
import paho.mqtt.client as mqtt
import json
import numpy as np
from PIL import Image
import io
from bokeh.models import Button, CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
 
# =========================================================
# IMPORTANTE: Instala estas dependencias antes de correr
# pip install streamlit paho-mqtt bokeh streamlit-bokeh-events
# pip install tensorflow pillow numpy
#
# Descarga tu modelo de Teachable Machine:
# 1. Ve a teachablemachine.withgoogle.com
# 2. Entrena con clases: "dueno" y "desconocido"
# 3. Exporta como TensorFlow > Keras (.h5)
# 4. Descarga keras_model.h5 y labels.txt
# 5. Ponlos en la misma carpeta que este script
# =========================================================
 
# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================
st.set_page_config(
    page_title="Guardian Vision",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# =========================================================
# ESTILOS
# =========================================================
st.markdown("""
<style>
.stApp { background-color: white !important; }
html, body, [class*="css"] { color: black !important; }
section[data-testid="stSidebar"] { background-color: #f3f4f6 !important; }
section[data-testid="stSidebar"] * { color: black !important; }
.header-box {
    background: linear-gradient(90deg, #111827, #2563eb);
    padding: 25px; border-radius: 18px;
    text-align: center; color: white !important; margin-bottom: 20px;
}
.card {
    background-color: white; padding: 25px; border-radius: 18px;
    border: 2px solid #d1d5db;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08); margin-bottom: 20px;
}
.stButton > button {
    width: 100%; background-color: #2563eb !important;
    color: white !important; font-size: 18px !important;
    font-weight: bold !important; border-radius: 12px !important;
    border: none !important; padding: 12px !important; margin-top: 8px !important;
}
div.bk-root {
    display: flex !important; justify-content: center !important;
    width: 100% !important; margin-top: 10px !important; margin-bottom: 10px !important;
}
</style>
""", unsafe_allow_html=True)
 
# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="header-box">
    <h1>🛡️ GUARDIAN VISION</h1>
    <h3>Sistema Inteligente de Seguridad | Voz + Cámara + MQTT</h3>
</div>
""", unsafe_allow_html=True)
 
# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.title("📘 Instrucciones")
    st.write("### 🎙️ Control por Voz")
    st.write("Presiona ESCUCHAR y di:")
    st.write("- **'abre la puerta'** → abre y enciende LED verde")
    st.write("- **'cierra la puerta'** → cierra y enciende LED rojo")
    st.write("### 📸 Reconocimiento Facial")
    st.write("1. Toma una foto con la cámara")
    st.write("2. Si eres el dueño → puerta ABRE (LED verde)")
    st.write("3. Si es desconocido → ALERTA (LED rojo)")
    st.write("### ⚙️ Configuración del Modelo")
    st.write("Coloca en la misma carpeta:")
    st.code("keras_model.h5\nlabels.txt")
    st.write("Clases esperadas en labels.txt:")
    st.code("0 dueno\n1 desconocido")
 
# =========================================================
# MQTT — topic y payload alineados con el ESP32
# =========================================================
BROKER = "broker.mqttdashboard.com"
PORT = 1883
TOPIC = "IMIA"   # mismo topic que el ESP32
 
@st.cache_resource
def setup_mqtt():
    client = mqtt.Client(client_id="GUARDIAN_VISION")
    try:
        client.connect(BROKER, PORT, 60)
    except Exception as e:
        st.warning(f"MQTT no conectado: {e}")
    return client
 
mqtt_client = setup_mqtt()
 
def enviar_mqtt(accion: str):
    """
    accion: "Abre" o "Cierra"
    Payload esperado por el ESP32: {"gesto": "Abre"} o {"gesto": "Cierra"}
    """
    try:
        payload = json.dumps({"gesto": accion})
        mqtt_client.publish(TOPIC, payload)
        return True
    except Exception as e:
        st.error(f"Error MQTT: {e}")
        return False
 
# =========================================================
# CARGAR MODELO TEACHABLE MACHINE
# =========================================================
@st.cache_resource
def cargar_modelo():
    """
    Carga el modelo exportado de Teachable Machine.
    Retorna (modelo, labels) o (None, None) si no existe.
    """
    try:
        import tensorflow as tf
        modelo = tf.keras.models.load_model("keras_model.h5", compile=False)
        with open("labels.txt", "r") as f:
            labels = [line.strip().split(" ", 1)[1] for line in f.readlines()]
        return modelo, labels
    except FileNotFoundError:
        return None, None
    except Exception as e:
        st.error(f"Error cargando modelo: {e}")
        return None, None
 
modelo, labels = cargar_modelo()
 
def clasificar_imagen(imagen_pil):
    """
    Recibe una imagen PIL, la preprocesa y retorna (clase, confianza).
    Teachable Machine espera imágenes 224x224 normalizadas a [-1, 1].
    """
    if modelo is None:
        return None, 0.0
    try:
        img = imagen_pil.convert("RGB").resize((224, 224))
        arr = np.array(img, dtype=np.float32)
        arr = (arr / 127.5) - 1.0          # normalización Teachable Machine
        arr = np.expand_dims(arr, axis=0)   # shape (1, 224, 224, 3)
        predicciones = modelo.predict(arr, verbose=0)
        idx = np.argmax(predicciones[0])
        confianza = float(predicciones[0][idx])
        clase = labels[idx] if labels else str(idx)
        return clase, confianza
    except Exception as e:
        st.error(f"Error en clasificación: {e}")
        return None, 0.0
 
# =========================================================
# SESSION STATE
# =========================================================
if "puerta_abierta" not in st.session_state:
    st.session_state.puerta_abierta = False
if "ultimo_comando" not in st.session_state:
    st.session_state.ultimo_comando = "Sin comandos aún"
if "ultimo_resultado_facial" not in st.session_state:
    st.session_state.ultimo_resultado_facial = ""
 
# =========================================================
# LAYOUT
# =========================================================
col1, col2 = st.columns([1, 2])
 
# =========================================================
# PANEL IZQUIERDO — Voz + Estado + Botones manuales
# =========================================================
with col1:
 
    if st.session_state.puerta_abierta:
        panel_bg    = "#dcfce7"
        panel_border= "#16a34a"
        panel_text  = "#166534"
        estado_texto= "🟢 PUERTA ABIERTA"
    else:
        panel_bg    = "#fee2e2"
        panel_border= "#dc2626"
        panel_text  = "#991b1b"
        estado_texto= "🔴 PUERTA CERRADA"
 
    st.markdown(f"""
    <div style="background-color:{panel_bg};padding:25px;border-radius:18px;
                border:3px solid {panel_border};margin-bottom:20px;">
        <h2 style="color:black;text-align:center;">🎙️ Control por Voz</h2>
    </div>
    """, unsafe_allow_html=True)
 
    # ----- BOTÓN VOZ -----
    stt_button = Button(label="🎙️ ESCUCHAR", width=240, height=70)
    stt_button.js_on_event("button_click", CustomJS(code="""
        var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SR) { alert("El navegador no soporta reconocimiento de voz"); return; }
        var r = new SR();
        r.lang = 'es-ES'; r.continuous = false; r.interimResults = false;
        r.onresult = function(e) {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: e.results[0][0].transcript}));
        };
        r.onerror = function(e) { console.log("Error voz:", e.error); };
        r.start();
    """))
 
    result = streamlit_bokeh_events(
        stt_button, events="GET_TEXT", key="listen",
        refresh_on_update=False, override_height=90, debounce_time=0
    )
 
    # ----- PROCESAR VOZ -----
    if result and "GET_TEXT" in result:
        comando = result.get("GET_TEXT", "").strip().lower()
        st.session_state.ultimo_comando = f"🎤 {comando}"
        st.success(f"Se escuchó: **{comando}**")
 
        palabras_abrir = ["abre", "abrir", "abre la puerta", "abrir puerta", "open"]
        palabras_cerrar= ["cierra", "cerrar", "cierra la puerta", "cerrar puerta", "close"]
 
        if any(p in comando for p in palabras_abrir):
            if enviar_mqtt("Abre"):
                st.session_state.puerta_abierta = True
                st.success("🟢 Puerta ABIERTA — LED verde encendido")
        elif any(p in comando for p in palabras_cerrar):
            if enviar_mqtt("Cierra"):
                st.session_state.puerta_abierta = False
                st.warning("🔴 Puerta CERRADA — LED rojo encendido")
        else:
            st.error("⚠️ Comando no reconocido. Di 'abre la puerta' o 'cierra la puerta'.")
 
    # ----- ÚLTIMO COMANDO -----
    st.markdown("<h3 style='color:black;'>🗣️ Último comando:</h3>", unsafe_allow_html=True)
    st.info(st.session_state.ultimo_comando)
 
    # ----- BOTONES MANUALES -----
    if st.button("🟢 ABRIR PUERTA"):
        if enviar_mqtt("Abre"):
            st.session_state.puerta_abierta = True
            st.session_state.ultimo_comando = "Apertura manual"
            st.success("🟢 Puerta abierta manualmente")
 
    if st.button("🔴 CERRAR PUERTA"):
        if enviar_mqtt("Cierra"):
            st.session_state.puerta_abierta = False
            st.session_state.ultimo_comando = "Cierre manual"
            st.warning("🔴 Puerta cerrada manualmente")
 
    # ----- ESTADO DEL SISTEMA -----
    st.markdown(f"""
    <div style="background-color:{panel_bg};padding:20px;border-radius:15px;
                border:3px solid {panel_border};text-align:center;margin-top:20px;">
        <h3 style="color:black;">📡 Estado del Sistema</h3>
        <h2 style="color:{panel_text};">{estado_texto}</h2>
    </div>
    """, unsafe_allow_html=True)
 
    # ----- ESTADO DEL MODELO -----
    if modelo is not None:
        st.success(f"✅ Modelo cargado | Clases: {', '.join(labels)}")
    else:
        st.warning("⚠️ keras_model.h5 no encontrado. Solo funcionará control por voz.")
 
# =========================================================
# PANEL DERECHO — Cámara + Reconocimiento Facial
# =========================================================
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h2 style='color:black;'>📸 Reconocimiento Facial</h2>", unsafe_allow_html=True)
 
    # Umbral de confianza configurable
    umbral = st.slider("Umbral de confianza para reconocer al dueño", 0.5, 1.0, 0.85, 0.05)
 
    foto = st.camera_input("Toma una foto para verificar identidad")
 
    if foto is not None:
        imagen = Image.open(foto)
        st.image(imagen, caption="Foto capturada", use_container_width=True)
 
        if modelo is not None:
            with st.spinner("Analizando identidad..."):
                clase, confianza = clasificar_imagen(imagen)
 
            st.markdown(f"**Resultado:** `{clase}` con `{confianza*100:.1f}%` de confianza")
 
            if clase == "dueno" and confianza >= umbral:
                # ✅ Es el dueño → abrir puerta
                enviar_mqtt("Abre")
                st.session_state.puerta_abierta = True
                st.session_state.ultimo_resultado_facial = f"✅ Dueño reconocido ({confianza*100:.1f}%)"
                st.session_state.ultimo_comando = "Reconocimiento facial exitoso"
                st.success(f"✅ ¡Dueño reconocido! Puerta abierta — LED verde encendido")
                st.balloons()
 
            elif clase == "dueno" and confianza < umbral:
                # Parecido pero debajo del umbral
                enviar_mqtt("Cierra")
                st.session_state.puerta_abierta = False
                st.session_state.ultimo_resultado_facial = f"⚠️ Confianza baja ({confianza*100:.1f}%)"
                st.warning(f"⚠️ Confianza baja ({confianza*100:.1f}%). Intenta de nuevo con mejor iluminación.")
 
            else:
                # ❌ Desconocido → cerrar y alertar
                enviar_mqtt("Cierra")
                st.session_state.puerta_abierta = False
                st.session_state.ultimo_resultado_facial = f"🚨 Desconocido detectado ({confianza*100:.1f}%)"
                st.session_state.ultimo_comando = "Intento de acceso denegado"
                st.error(f"🚨 ACCESO DENEGADO — Persona no reconocida. LED rojo encendido.")
 
        else:
            # Sin modelo: solo muestra la foto como monitoreo
            st.info("📷 Monitoreo activo (carga keras_model.h5 para activar reconocimiento facial)")
            if st.session_state.puerta_abierta:
                st.warning("⚠️ Presencia detectada con puerta abierta")
 
        # Último resultado facial
        if st.session_state.ultimo_resultado_facial:
            st.markdown(f"**Último análisis:** {st.session_state.ultimo_resultado_facial}")
 
    else:
        st.markdown(
            "<h3 style='color:black;text-align:center;'>📷 Esperando captura...</h3>",
            unsafe_allow_html=True
        )
 
    st.markdown('</div>', unsafe_allow_html=True)
 
# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.markdown(
    "<p style='color:black;text-align:center;'>Guardian Vision © Proyecto Interfaces Multimodales | "
    "Angie Vargas · Isabella Saldarriaga · Salomé Rivero</p>",
    unsafe_allow_html=True
)
 
