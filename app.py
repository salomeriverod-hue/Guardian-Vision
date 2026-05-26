# =========================================================
# GUARDIAN VISION - VOZ + TEACHABLE MACHINE + WOKWI
# =========================================================

import streamlit as st
import paho.mqtt.client as mqtt
import json
from PIL import Image
from bokeh.models import Button, CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import numpy as np
import tensorflow as tf

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
    st.write("- abrir puerta")
    st.write("- cerrar puerta")

    st.write("### 🔘 Control Manual")
    st.write("- Abrir puerta")
    st.write("- Cerrar puerta")

    st.write("### 📸 Reconocimiento Facial")
    st.write("Clases:")
    st.code("dueno\ndueno2\ndesconocido")

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
    except:
        pass

    return client

mqtt_client = setup_mqtt()

# =========================================================
# FUNCIÓN MQTT
# =========================================================
def enviar_mqtt(mensaje):

    try:

        payload = json.dumps({
            "gesto": mensaje
        })

        mqtt_client.publish(TOPIC, payload)

    except:
        pass

# =========================================================
# CARGAR MODELO
# =========================================================
@st.cache_resource
def cargar_modelo():

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

# =========================================================
# CLASIFICAR IMAGEN
# =========================================================
def clasificar_imagen(imagen_pil):

    img = imagen_pil.convert("RGB").resize((224, 224))

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

if "ultimo_comando" not in st.session_state:
    st.session_state.ultimo_comando = "Sin comandos aún"

# =========================================================
# LAYOUT
# =========================================================
col1, col2 = st.columns([1,2])

# =========================================================
# PANEL IZQUIERDO
# =========================================================
with col1:

    if st.session_state.puerta_abierta:

        panel_bg = "#dcfce7"
        panel_border = "#16a34a"
        panel_text = "#166534"
        estado_texto = "🟢 PUERTA ABIERTA"

    else:

        panel_bg = "#fee2e2"
        panel_border = "#dc2626"
        panel_text = "#991b1b"
        estado_texto = "🔴 PUERTA CERRADA"

    st.markdown(f"""
    <div style="
        background-color:{panel_bg};
        padding:25px;
        border-radius:18px;
        border:3px solid {panel_border};
        margin-bottom:20px;
    ">
        <h2 style="color:black; text-align:center;">
        🎙️ Control Inteligente
        </h2>
    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # BOTÓN VOZ
    # =====================================================
    st.write("🎙️ Toca el botón y habla")

    stt_button = Button(label="🎤 ESCUCHAR", width=240, height=70)

    stt_button.js_on_event("button_click", CustomJS(code="""
        var recognition = new webkitSpeechRecognition();

        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "es-ES";

        recognition.onresult = function (e) {

            var value = "";

            for (var i = e.resultIndex; i < e.results.length; ++i) {

                if (e.results[i].isFinal) {

                    value += e.results[i][0].transcript;
                }
            }

            if (value != "") {

                document.dispatchEvent(
                    new CustomEvent("GET_TEXT", {
                        detail: value
                    })
                );
            }
        };

        recognition.start();
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
    # PROCESAR VOZ
    # =====================================================
    if result:

        if "GET_TEXT" in result:

            comando = result.get("GET_TEXT").strip().lower()

            st.success(f"🎤 Se escuchó: {comando}")

            st.session_state.ultimo_comando = comando

            # =============================================
            # ABRIR
            # =============================================
            if (
                "abrir" in comando or
                "abre" in comando or
                "abrir puerta" in comando or
                "abre la puerta" in comando
            ):

                st.success("🟢 PUERTA ABIERTA")

                st.session_state.puerta_abierta = True

                enviar_mqtt("Abre")

            # =============================================
            # CERRAR
            # =============================================
            elif (
                "cerrar" in comando or
                "cierra" in comando or
                "cerrar puerta" in comando or
                "cierra la puerta" in comando
            ):

                st.error("🔴 PUERTA CERRADA")

                st.session_state.puerta_abierta = False

                enviar_mqtt("Cierra")

            else:

                st.warning("⚠️ Comando no reconocido")

    # =====================================================
    # ÚLTIMO COMANDO
    # =====================================================
    st.markdown(
        "<h3 style='color:black;'>🗣️ Último comando:</h3>",
        unsafe_allow_html=True
    )

    st.info(st.session_state.ultimo_comando)

    # =====================================================
    # BOTONES MANUALES
    # =====================================================
    if st.button("🟢 ABRIR PUERTA"):

        st.session_state.puerta_abierta = True

        st.session_state.ultimo_comando = "Apertura manual"

        enviar_mqtt("Abre")

    if st.button("🔴 CERRAR PUERTA"):

        st.session_state.puerta_abierta = False

        st.session_state.ultimo_comando = "Cierre manual"

        enviar_mqtt("Cierra")

    # =====================================================
    # ESTADO
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
        <h2 style="color:{panel_text};">
        {estado_texto}
        </h2>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# PANEL DERECHO
# =========================================================
with col2:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(
        "<h2 style='color:black;'>📸 Reconocimiento Facial</h2>",
        unsafe_allow_html=True
    )

    foto = st.camera_input("Toma una captura")

    if foto is not None:

        imagen = Image.open(foto)

        st.image(
            imagen,
            caption="Captura actual",
            use_container_width=True
        )

        clase, confianza = clasificar_imagen(imagen)

        porcentaje = confianza * 100

        st.write(f"Clase detectada: {clase}")

        st.write(f"Confianza: {porcentaje:.1f}%")

        dueños = ["dueno", "dueno2"]

        # =================================================
        # DUEÑO
        # =================================================
        if clase.lower() in dueños and porcentaje >= 40:

            st.success("✅ Dueño reconocido")

            st.write(f"Acceso permitido ({porcentaje:.1f}%)")

            st.session_state.puerta_abierta = True

            enviar_mqtt("Abre")

        # =================================================
        # DESCONOCIDO
        # =================================================
        else:

            st.error("🚨 PERSONA DESCONOCIDA")

            st.write(f"Acceso denegado ({porcentaje:.1f}%)")

            st.session_state.puerta_abierta = False

            enviar_mqtt("Cierra")

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
    "<p style='color:black; text-align:center;'>"
    "Guardian Vision © Proyecto Interfaces Multimodales | "
    "Angie Vargas - Isabella Saldarriaga - Salome Rivero"
    "</p>",
    unsafe_allow_html=True
)
