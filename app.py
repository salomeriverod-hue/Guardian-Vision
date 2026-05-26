# =========================================================
# GUARDIAN VISION - CÓDIGO COMPLETO CON VOZ CORREGIDA
# =========================================================

import streamlit as st
import paho.mqtt.client as mqtt
import json
from PIL import Image, ImageOps
import numpy as np
from bokeh.models import Button, CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

# --- Librerías añadidas para Teachable Machine de forma segura ---
try:
    import tensorflow as tf
    from keras.models import load_model
except ImportError:
    pass

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
.stApp {
    background-color: white !important;
}

html, body, [class*="css"] {
    color: black !important;
}

section[data-testid="stSidebar"] {
    background-color: #f3f4f6 !important;
}

section[data-testid="stSidebar"] * {
    color: black !important;
}

.header-box {
    background: linear-gradient(90deg, #111827, #2563eb);
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    color: white !important;
    margin-bottom: 20px;
}

.card {
    background-color: white;
    padding: 25px;
    border-radius: 18px;
    border: 2px solid #d1d5db;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.stButton > button {
    width: 100%;
    background-color: #2563eb !important;
    color: white !important;
    font-size: 18px !important;
    font-weight: bold !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 12px !important;
    margin-top: 8px !important;
}

div.bk-root {
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
    margin-top: 10px !important;
    margin-bottom: 10px !important;
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
    st.write("- enciende la alarma")
    st.write("- apaga la alarma")
    st.write("- **Palabra Clave:** 'abrete sesamo' para desbloquear.")

    st.write("### 🔘 Control Manual")
    st.write("- Botón ENCENDER")
    st.write("- Botón APAGAR")

    st.write("### 📸 Vigilancia")
    st.write("Toma una foto para monitorear.")
    st.write("Si la alarma está activa, enviará alerta MQTT.")

# =========================================================
# MQTT
# =========================================================
BROKER = "broker.mqttdashboard.com"
PORT = 1883
TOPIC = "voice_ctrl"

@st.cache_resource
def setup_mqtt():
    # Mantenemos compatibilidad universal con librerías Paho antiguas y nuevas
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id="ANGIE_GUARD")
    except AttributeError:
        client = mqtt.Client(client_id="ANGIE_GUARD")
    try:
        client.connect(BROKER, PORT, 60)
    except:
        pass
    return client

mqtt_client = setup_mqtt()

# =========================================================
# SESSION STATE
# =========================================================
if "alarma_activa" not in st.session_state:
    st.session_state.alarma_activa = False

if "ultimo_comando" not in st.session_state:
    st.session_state.ultimo_comando = "Sin comandos aún"

# --- Nuevas variables de estado para la Puerta Inteligente ---
if "intentos_fallidos" not in st.session_state:
    st.session_state.intentos_fallidos = 0

if "puerta_desbloqueada" not in st.session_state:
    st.session_state.puerta_desbloqueada = False

# =========================================================
# FUNCIÓN MQTT
# =========================================================
def enviar_mqtt(mensaje):
    try:
        payload = json.dumps({"Act1": mensaje})
        mqtt_client.publish(TOPIC, payload)
    except:
        pass

# =========================================================
# FUNCIÓN MODELO TEACHABLE MACHINE
# =========================================================
@st.cache_resource
def cargar_modelo_tm():
    try:
        model = load_model("keras_model.h5", compile=False)
        with open("labels.txt", "r") as f:
            class_names = f.readlines()
        return model, class_names
    except:
        return None, None

modelo_tm, clases_tm = cargar_modelo_tm()

# =========================================================
# LÓGICA DE ALERTA GLOBAL (Aviso grande si supera 2 intentos)
# =========================================================
if st.session_state.intentos_fallidos >= 2:
    st.markdown("""
    <div style="background-color:#7f1d1d; padding:30px; border-radius:15px; border:5px solid #ef4444; text-align:center; margin-bottom:20px;">
        <h1 style="color:#fca5a5 !important; font-size:45px; font-weight:bold; margin:0;">🚨 ALERTA MÁXIMA: SISTEMA BLOQUEADO 🚨</h1>
        <p style="color:white !important; font-size:20px; margin-top:10px;">Se han superado los 2 intentos de acceso fallidos. Puerta asegurada.</p>
    </div>
    """, unsafe_allow_html=True)
    enviar_mqtt("intruso") # Envía alerta al Wokwi de inmediato

# =========================================================
# LAYOUT
# =========================================================
col1, col2 = st.columns([1, 2])

# =========================================================
# PANEL IZQUIERDO
# =========================================================
with col1:

    # ESTADO (Modificado visualmente si la puerta se desbloquea exitosamente)
    if st.session_state.puerta_desbloqueada:
        panel_bg = "#dcfce7"
        panel_border = "#16a34a"
        panel_text = "#166534"
        estado_texto = "🔓 PUERTA DESBLOQUEADA"
    elif st.session_state.alarma_activa:
        panel_bg = "#dcfce7"
        panel_border = "#16a34a"
        panel_text = "#166534"
        estado_texto = "🟢 ALARMA ACTIVADA"
    else:
        panel_bg = "#fee2e2"
        panel_border = "#dc2626"
        panel_text = "#991b1b"
        estado_texto = "🔴 ALARMA DESACTIVADA"

    # TÍTULO
    st.markdown(f"""
    <div style="
        background-color:{panel_bg};
        padding:25px;
        border-radius:18px;
        border:3px solid {panel_border};
        margin-bottom:20px;
    ">
        <h2 style="color:black; text-align:center;">🎙️ Control Inteligente</h2>
    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # BOTÓN VOZ
    # =====================================================
    stt_button = Button(label="🎙️ ESCUCHAR", width=240, height=70)

    stt_button.js_on_event("button_click", CustomJS(code="""
        var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            alert("El navegador no soporta reconocimiento de voz");
        } else {
            var recognition = new SpeechRecognition();

            recognition.lang = 'es-ES';
            recognition.continuous = false;
            recognition.interimResults = false;

            recognition.onresult = function(e) {
                var value = e.results[0][0].transcript;

                document.dispatchEvent(
                    new CustomEvent("GET_TEXT", {
                        detail: value
                    })
                );
            };

            recognition.onerror = function(e) {
                console.log("Error:", e.error);
            };

            recognition.start();
        }
    """))

    result = streamlit_bokeh_events(
        stt_button,
        events="GET_TEXT",
        key="listen",
        refresh_on_update=False,
        override_height=90,
        debounce_time=0
    )

    # =====================================================
    # PROCESAR VOZ COMPLEMENTADO
    # =====================================================
    if result:
        if "GET_TEXT" in result:
            comando = result.get("GET_TEXT", "").strip().lower()
            st.session_state.ultimo_comando = comando

            # --- NUEVA LÓGICA: OPCIÓN 1 - PALABRA CLAVE ---
            if "abrete sesamo" in comando:
                st.session_state.puerta_desbloqueada = True
                st.session_state.intentos_fallidos = 0 # Reinicia intentos
                enviar_mqtt("verde_on") # Comando específico para encender bombillo verde
                st.balloons()
            
            # Comandos base respetados
            elif (
                "enciende la alarma" in comando or
                "activar alarma" in comando or
                "enciende alarma" in comando or
                "activar" in comando or
                "encender" in comando
            ):
                st.session_state.alarma_activa = True
                enviar_mqtt("activado")
                st.success("🟢 Alarma ACTIVADA")

            elif (
                "apaga la alarma" in comando or
                "desactiva la alarma" in comando or
                "apaga alarma" in comando or
                "desactivar" in comando or
                "apagar" in comando
            ):
                st.session_state.alarma_activa = False
                st.session_state.puerta_desbloqueada = False
                enviar_mqtt("desactivado")
                st.warning("🔴 Alarma DESACTIVADA")

            # Si dice otra frase que no coincide con la palabra clave ni comandos base
            else:
                st.session_state.intentos_fallidos += 1
                st.session_state.puerta_desbloqueada = False
                enviar_mqtt("rojo_on") # Enciende bombillo rojo en Wokwi
                st.error(f"⚠️ Palabra clave incorrecta. Intentos fallidos: {st.session_state.intentos_fallidos}/2")

    # =====================================================
    # ÚLTIMO COMANDO
    # =====================================================
    st.markdown("<h3 style='color:black;'>🗣️ Último comando:</h3>", unsafe_allow_html=True)
    st.info(st.session_state.ultimo_comando)

    # =====================================================
    # BOTONES MANUALES
    # =====================================================
    if st.button("🟢 ENCENDER ALARMA"):
        st.session_state.alarma_activa = True
        st.session_state.ultimo_comando = "Encendido manual"
        enviar_mqtt("activado")

    if st.button("🔴 APAGAR ALARMA"):
        st.session_state.alarma_activa = False
        st.session_state.puerta_desbloqueada = False
        st.session_state.intentos_fallidos = 0
        st.session_state.ultimo_comando = "Apagado manual"
        enviar_mqtt("desactivado")

    # =====================================================
    # ESTADO DEL SISTEMA
    # =====================================================
    st.markdown(f"""
    <div style="
        background-color:{panel_bg};
        padding:20px;
        border-radius:15px;
        border:3px solid {panel_border};
        text-align:center;
        margin-top:20px;
    ">
        <h3 style="color:black;">📡 Estado del Sistema</h3>
        <h2 style="color:{panel_text};">{estado_texto}</h2>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# PANEL DERECHO - CÁMARA (CON RECONOCIMIENTO FACIAL TM)
# =========================================================
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h2 style='color:black;'>📸 Cámara de Vigilancia</h2>", unsafe_allow_html=True)

    foto = st.camera_input("Toma una captura de seguridad")

    if foto is not None:
        imagen = Image.open(foto)
        st.image(imagen, caption="Captura actual", use_container_width=True)

        # --- NUEVA LÓGICA: OPCIÓN 2 - RECONOCIMIENTO FACIAL TEACHABLE MACHINE ---
        if modelo_tm is not None:
            # Adecuar la imagen para el formato requerido por Teachable Machine
            size = (224, 224)
            image_resized = ImageOps.fit(imagen, size, Image.Resampling.LENS)
            image_array = np.asarray(image_resized)
            normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
            data = np.reshape(normalized_image_array, (1, 224, 224, 3))

            # Predicción
            prediction = modelo_tm.predict(data)
            index = np.argmax(prediction)
            class_name = clases_tm[index].strip()
            confidence_score = prediction[0][index]

            st.write(f"**Resultado Escaneo:** {class_name} ({confidence_score*100:.2f}%)")

            # Supongamos que tu clase index 0 en labels.txt es "Dueno" o "Propietario"
            if "dueno" in class_name.lower() or "propietario" in class_name.lower() and confidence_score > 0.80:
                st.session_state.puerta_desbloqueada = True
                st.session_state.intentos_fallidos = 0
                st.success("🔓 Rostro reconocido. ¡Acceso concedido!")
                enviar_mqtt("verde_on")
            else:
                st.session_state.intentos_fallidos += 1
                st.session_state.puerta_desbloqueada = False
                st.error("❌ Rostro Desconocido. Acceso denegado.")
                enviar_mqtt("rojo_on")
        else:
            # Lógica alternativa por si no se encuentra el archivo .h5 del modelo en GitHub
            if st.session_state.alarma_activa:
                st.error("🚨 ALERTA: Presencia detectada")
                enviar_mqtt("intruso")
            else:
                st.success("✅ Monitoreo realizado (alarma apagada)")

    else:
        st.markdown(
            "<h3 style='color:black; text-align:center;'>📷 Esperando captura...</h3>",
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.markdown(
    "<p style='color:black; text-align:center;'>Guardian Vision ©️ Proyecto Interfaces Multimodales | Angie Vargas - Isabella Saldarriaga - Salome Rivero</p>",
    unsafe_allow_html=True
)
