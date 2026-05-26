import streamlit as st
import paho.mqtt.client as mqtt
import json
import numpy as np
from PIL import Image
from bokeh.models import Button, CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from datetime import datetime

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

st.set_page_config(
    page_title="Guardian Vision",
    page_icon="🛡️",
    layout="wide"
)

# =========================================================
# ESTILOS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: white;
}

html, body, [class*="css"]  {
    color: black !important;
}

.header-box {
    background: linear-gradient(90deg, #111827, #2563eb);
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    color: white;
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
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="header-box">
    <h1>🛡️ GUARDIAN VISION</h1>
    <h3>Sistema Inteligente de Seguridad</h3>
</div>
""", unsafe_allow_html=True)

# =========================================================
# MQTT
# =========================================================

BROKER = "broker.mqttdashboard.com"
PORT = 1883
TOPIC = "IMIA"

@st.cache_resource
def setup_mqtt():

    client = mqtt.Client(client_id="GUARDIAN_VISION")

    try:
        client.connect(BROKER, PORT, 60)
    except Exception as e:
        st.error(e)

    return client

mqtt_client = setup_mqtt()

def enviar_mqtt(accion):

    payload = json.dumps({
        "gesto": accion
    })

    mqtt_client.publish(TOPIC, payload)

# =========================================================
# MODELO TEACHABLE MACHINE
# =========================================================

@st.cache_resource
def cargar_modelo():

    import tensorflow as tf

    modelo = tf.keras.models.load_model(
        "keras_model.h5",
        compile=False
    )

    with open("labels.txt", "r") as f:

        labels = [
            line.strip().split(" ", 1)[1]
            for line in f.readlines()
        ]

    return modelo, labels

modelo, labels = cargar_modelo()

def clasificar_imagen(imagen_pil):

    img = imagen_pil.convert("RGB").resize((224,224))

    arr = np.array(img, dtype=np.float32)

    arr = (arr / 127.5) - 1

    arr = np.expand_dims(arr, axis=0)

    predicciones = modelo.predict(arr, verbose=0)

    idx = np.argmax(predicciones[0])

    confianza = float(predicciones[0][idx])

    clase = labels[idx]

    return clase, confianza

# =========================================================
# SESSION STATE
# =========================================================

if "puerta_abierta" not in st.session_state:
    st.session_state.puerta_abierta = False

if "logs" not in st.session_state:
    st.session_state.logs = []

# =========================================================
# LAYOUT
# =========================================================

col1, col2 = st.columns([1,2])

# =========================================================
# PANEL IZQUIERDO
# =========================================================

with col1:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🎙️ Control por Voz")

    st.write("Di:")
    st.write("- abre la puerta")
    st.write("- cierra la puerta")

    stt_button = Button(
        label="🎤 ESCUCHAR",
        width=220,
        height=70
    )

    stt_button.js_on_event("button_click", CustomJS(code="""
        var SR = window.SpeechRecognition || window.webkitSpeechRecognition;

        var r = new SR();

        r.lang = 'es-ES';

        r.onresult = function(e) {

            document.dispatchEvent(
                new CustomEvent(
                    "GET_TEXT",
                    {detail: e.results[0][0].transcript}
                )
            );
        };

        r.start();
    """))

    result = streamlit_bokeh_events(
        stt_button,
        events="GET_TEXT",
        key="listen"
    )

    if result and "GET_TEXT" in result:

        comando = result["GET_TEXT"].lower()

        if "abre" in comando:

            enviar_mqtt("Abre")

            st.session_state.puerta_abierta = True

            st.success("🟢 Puerta abierta")

            st.session_state.logs.append(
                f"{datetime.now().strftime('%H:%M:%S')} - Apertura por voz"
            )

        elif "cierra" in comando:

            enviar_mqtt("Cierra")

            st.session_state.puerta_abierta = False

            st.error("🔴 Puerta cerrada")

            st.session_state.logs.append(
                f"{datetime.now().strftime('%H:%M:%S')} - Cierre por voz"
            )

    st.subheader("⚙️ Control Manual")

    manual = st.toggle("Activar / Desactivar")

    if manual:

        enviar_mqtt("Abre")

        st.session_state.puerta_abierta = True

    else:

        enviar_mqtt("Cierra")

        st.session_state.puerta_abierta = False

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# PANEL DERECHO
# =========================================================

with col2:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📸 Reconocimiento Facial")

    umbral = st.slider(
        "Umbral de confianza",
        0.5,
        1.0,
        0.85
    )

    foto = st.camera_input(
        "Toma una foto"
    )

    if foto is not None:

        imagen = Image.open(foto)

        st.image(imagen)

        clase, confianza = clasificar_imagen(imagen)

        st.write(f"Clase: {clase}")
        st.write(f"Confianza: {confianza*100:.1f}%")

        dueños = ["dueno", "dueno2"]

        if clase.lower() in dueños and confianza >= umbral:

            enviar_mqtt("Abre")

            st.session_state.puerta_abierta = True

            st.success("🟢 Dueño reconocido")

            st.balloons()

            st.session_state.logs.append(
                f"{datetime.now().strftime('%H:%M:%S')} - Reconocimiento facial exitoso"
            )

        else:

            enviar_mqtt("Alarma")

            st.session_state.puerta_abierta = False

            st.error("🚨 PERSONA DESCONOCIDA")

            st.session_state.logs.append(
                f"{datetime.now().strftime('%H:%M:%S')} - Intruso detectado"
            )

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# HISTORIAL
# =========================================================

st.markdown("## 📋 Historial")

for log in reversed(st.session_state.logs[-10:]):
    st.write(log)
