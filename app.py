# =========================================================
# SMART DOOR - APLICACIÓN PRINCIPAL EN STREAMLIT
# =========================================================
# Aplicación de puerta inteligente con reconocimiento de voz y facial
# Conectada a Wokwi mediante MQTT
# =========================================================

import streamlit as st
import paho.mqtt.client as mqtt
import json
from PIL import Image
import cv2
import numpy as np
from bokeh.models import Button, CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import time
from datetime import datetime
import threading

# =========================================================
# CONFIGURACIÓN
# =========================================================
st.set_page_config(
    page_title="Smart Door - Sistema de Seguridad",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# INFORMACIÓN DEL PROYECTO
# =========================================================
WOKWI_PROJECT_URL = "https://wokwi.com/projects/465100849740681217"
WOKWI_LED_RED = "D5"   # GPIO 5
WOKWI_LED_GREEN = "D18"  # GPIO 18

# =========================================================
# CONFIGURACIÓN MQTT
# =========================================================
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_PORT = 1883
MQTT_TOPIC_COMMAND = "smart_door/command"
MQTT_TOPIC_STATUS = "smart_door/status"
MQTT_CLIENT_ID = "SMART_DOOR_APP"

# GPIO Wokwi
GPIO_LED_RED = 5
GPIO_LED_GREEN = 18

# =========================================================
# CONFIGURACIÓN TEACHABLE MACHINE
# =========================================================
# URL del modelo entrenado (REEMPLAZAR CON TU URL)
TEACHABLE_MACHINE_URL = "https://teachablemachine.withgoogle.com/models/TU_MODELO_ID/"

# Clases entrenadas (2 dueños)
VALID_FACIAL_CLASSES = ["Dueño 1", "Dueño 2"]

# Confianza mínima para aceptar (0-1)
MIN_FACIAL_CONFIDENCE = 0.70  # 70%

# =========================================================
# ESTILOS CSS
# =========================================================
st.markdown("""
<style>
* {
    margin: 0;
    padding: 0;
}

.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #e2e8f0;
}

/* Header */
.header-container {
    background: linear-gradient(90deg, #0f172a, #1e40af);
    padding: 40px 20px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 30px;
    border: 2px solid #3b82f6;
    box-shadow: 0 0 30px rgba(59, 130, 246, 0.3);
}

.header-container h1 {
    color: #60a5fa;
    font-size: 3em;
    margin-bottom: 10px;
    text-shadow: 0 0 20px rgba(96, 165, 250, 0.5);
}

.header-container p {
    color: #cbd5e1;
    font-size: 1.2em;
}

/* Cards */
.card {
    background: linear-gradient(135deg, #1e293b, #334155);
    padding: 25px;
    border-radius: 15px;
    border: 2px solid #475569;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    margin-bottom: 20px;
}

.card h2, .card h3 {
    color: #60a5fa;
    margin-bottom: 15px;
}

/* Status Badge */
.status-badge {
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    font-weight: bold;
    font-size: 1.3em;
    margin: 15px 0;
    border: 2px solid;
}

.status-unlocked {
    background: linear-gradient(135deg, #10b981, #059669);
    border-color: #34d399;
    color: white;
    box-shadow: 0 0 20px rgba(16, 185, 129, 0.4);
}

.status-locked {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    border-color: #f87171;
    color: white;
    box-shadow: 0 0 20px rgba(239, 68, 68, 0.4);
}

.status-warning {
    background: linear-gradient(135deg, #f59e0b, #d97706);
    border-color: #fbbf24;
    color: white;
    box-shadow: 0 0 20px rgba(245, 158, 11, 0.4);
}

/* Botones */
.stButton > button {
    background: linear-gradient(90deg, #3b82f6, #1e40af) !important;
    color: white !important;
    font-size: 16px !important;
    font-weight: bold !important;
    border-radius: 10px !important;
    border: 2px solid #60a5fa !important;
    padding: 12px 20px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 0 15px rgba(59, 130, 246, 0.3) !important;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #1e40af, #1e3a8a) !important;
    box-shadow: 0 0 25px rgba(59, 130, 246, 0.6) !important;
}

/* Alerts */
.alert-danger {
    background: linear-gradient(135deg, #dc2626, #991b1b);
    border: 2px solid #f87171;
    color: white;
    padding: 20px;
    border-radius: 12px;
    font-size: 1.2em;
    font-weight: bold;
    animation: pulse 1s infinite;
    margin: 20px 0;
}

.alert-success {
    background: linear-gradient(135deg, #10b981, #059669);
    border: 2px solid #34d399;
    color: white;
    padding: 20px;
    border-radius: 12px;
    font-size: 1.1em;
    margin: 20px 0;
}

.alert-warning {
    background: linear-gradient(135deg, #f59e0b, #d97706);
    border: 2px solid #fbbf24;
    color: white;
    padding: 20px;
    border-radius: 12px;
    font-size: 1.1em;
    margin: 20px 0;
}

@keyframes pulse {
    0%, 100% {
        opacity: 1;
    }
    50% {
        opacity: 0.7;
    }
}

/* Indicadores */
.indicator {
    display: inline-block;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    margin-right: 10px;
}

.indicator-on {
    background: #10b981;
    box-shadow: 0 0 15px #10b981;
}

.indicator-off {
    background: #6b7280;
    box-shadow: 0 0 10px #6b7280;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #0f172a, #1e293b) !important;
    border-right: 2px solid #3b82f6;
}

section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* Divider */
hr {
    border: 1px solid #3b82f6 !important;
    margin: 30px 0 !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #64748b;
    padding: 20px;
    border-top: 1px solid #475569;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SESIÓN STATE
# =========================================================
if "puerta_abierta" not in st.session_state:
    st.session_state.puerta_abierta = False

if "intentos_fallidos" not in st.session_state:
    st.session_state.intentos_fallidos = 0

if "ultimo_evento" not in st.session_state:
    st.session_state.ultimo_evento = "Esperando evento..."

if "historial_eventos" not in st.session_state:
    st.session_state.historial_eventos = []

if "alarma_activa" not in st.session_state:
    st.session_state.alarma_activa = False

if "mqtt_conectado" not in st.session_state:
    st.session_state.mqtt_conectado = False

# =========================================================
# CONFIGURAR MQTT
# =========================================================
@st.cache_resource
def setup_mqtt_client():
    client = mqtt.Client(client_id=MQTT_CLIENT_ID)
    
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            st.session_state.mqtt_conectado = True
            client.subscribe(MQTT_TOPIC_STATUS)
        else:
            st.session_state.mqtt_conectado = False
    
    def on_disconnect(client, userdata, rc):
        st.session_state.mqtt_conectado = False
    
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
    except Exception as e:
        pass
    
    return client

mqtt_client = setup_mqtt_client()

# =========================================================
# FUNCIONES MQTT
# =========================================================
def enviar_comando_mqtt(comando, dato):
    """Envía comando al ESP32 vía MQTT"""
    try:
        payload = json.dumps({
            "comando": comando,
            "dato": dato,
            "timestamp": datetime.now().isoformat()
        })
        mqtt_client.publish(MQTT_TOPIC_COMMAND, payload)
        return True
    except Exception as e:
        return False

def encender_led_verde():
    """Enciende LED verde en Wokwi"""
    enviar_comando_mqtt("LED", "GREEN_ON")

def encender_led_rojo():
    """Enciende LED rojo en Wokwi"""
    enviar_comando_mqtt("LED", "RED_ON")

def apagar_leds():
    """Apaga todos los LEDs"""
    enviar_comando_mqtt("LED", "ALL_OFF")

# =========================================================
# FUNCIONES DE LÓGICA
# =========================================================
def registrar_evento(tipo, descripcion):
    """Registra un evento en el historial"""
    evento = {
        "tipo": tipo,
        "descripcion": descripcion,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }
    st.session_state.historial_eventos.insert(0, evento)
    st.session_state.ultimo_evento = descripcion

def desbloquear_puerta():
    """Desbloquea la puerta"""
    st.session_state.puerta_abierta = True
    st.session_state.intentos_fallidos = 0
    st.session_state.alarma_activa = False
    encender_led_verde()
    registrar_evento("ÉXITO", "🔓 Puerta desbloqueada - Acceso concedido")

def bloquear_puerta():
    """Bloquea la puerta"""
    st.session_state.puerta_abierta = False
    apagar_leds()
    registrar_evento("BLOQUEO", "🔐 Puerta bloqueada")

def intento_fallido(razon):
    """Registra un intento fallido"""
    st.session_state.intentos_fallidos += 1
    encender_led_rojo()
    registrar_evento("ERROR", f"❌ Acceso denegado - {razon}")
    
    if st.session_state.intentos_fallidos >= 2:
        st.session_state.alarma_activa = True
        registrar_evento("ALARMA", "🚨 ALARMA ACTIVADA - 2+ intentos fallidos")

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="header-container">
    <h1>🔐 SMART DOOR</h1>
    <p>Sistema Inteligente de Seguridad | Reconocimiento de Voz + Facial + Wokwi MQTT</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR - INSTRUCCIONES Y STATUS
# =========================================================
with st.sidebar:
    st.title("📋 Panel de Control")
    
    st.subheader("🔗 Proyecto Wokwi")
    st.markdown(f"[**▶ Abrir Wokwi (en vivo)**]({WOKWI_PROJECT_URL})")
    st.caption(f"LED Rojo: {WOKWI_LED_RED} | LED Verde: {WOKWI_LED_GREEN}")
    
    st.divider()
    
    st.subheader("📡 Estado MQTT")
    if st.session_state.mqtt_conectado:
        st.success("✅ Conectado a Broker")
    else:
        st.error("❌ Desconectado del Broker")
    
    st.divider()
    
    st.subheader("🎤 Control por Voz")
    st.write("""
    - **Palabra clave:** "abrete sesamo"
    - Presiona el botón 🎙️ ESCUCHAR
    - Si es correcta → Puerta abierta
    - Si es incorrecta → Intento fallido
    """)
    
    st.subheader("👤 Reconocimiento Facial")
    st.write("""
    - Carga un modelo de Teachable Machine
    - La cámara detecta rostros
    - Si es reconocido → Puerta abierta
    - Si no → Intento fallido
    """)
    
    st.subheader("⚠️ Sistema de Alarma")
    st.write("""
    - Se activa tras 2 intentos fallidos
    - Muestra advertencia en pantalla
    - Todos los LEDs se encienden
    """)
    
    st.divider()
    
    st.subheader("📊 Estadísticas")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Intentos Fallidos", st.session_state.intentos_fallidos)
    with col2:
        estado = "🔓 ABIERTA" if st.session_state.puerta_abierta else "🔐 CERRADA"
        st.metric("Estado Puerta", estado)

# =========================================================
# LAYOUT PRINCIPAL
# =========================================================
col_izq, col_der = st.columns([1, 1], gap="large")

# =========================================================
# COLUMNA IZQUIERDA - RECONOCIMIENTO DE VOZ
# =========================================================
with col_izq:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🎤 Desbloqueo por Voz")
    st.write("Palabra clave: **'abrete sesamo'**")
    
    # Estado actual
    if st.session_state.puerta_abierta:
        estado_badge = "status-unlocked"
        estado_texto = "🔓 PUERTA DESBLOQUEADA"
    else:
        estado_badge = "status-locked"
        estado_texto = "🔐 PUERTA BLOQUEADA"
    
    st.markdown(f"""
    <div class="status-badge {estado_badge}">
        {estado_texto}
    </div>
    """, unsafe_allow_html=True)
    
    # Botón de voz con Bokeh
    st.write("**Presiona para activar micrófono:**")
    stt_button = Button(label="🎙️ ESCUCHAR", width=200, height=60)
    
    stt_button.js_on_event("button_click", CustomJS(code="""
        var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (!SpeechRecognition) {
            alert("Tu navegador no soporta reconocimiento de voz");
        } else {
            var recognition = new SpeechRecognition();
            recognition.lang = 'es-ES';
            recognition.continuous = false;
            recognition.interimResults = false;
            
            recognition.onstart = function() {
                console.log("Escuchando...");
            };
            
            recognition.onresult = function(e) {
                var transcript = e.results[0][0].transcript.toLowerCase().trim();
                document.dispatchEvent(new CustomEvent("VOICE_INPUT", {detail: transcript}));
            };
            
            recognition.onerror = function(e) {
                console.log("Error:", e.error);
            };
            
            recognition.start();
        }
    """))
    
    result = streamlit_bokeh_events(
        stt_button,
        events="VOICE_INPUT",
        key="voice_input",
        refresh_on_update=False,
        override_height=80,
        debounce_time=0
    )
    
    # Procesar entrada de voz
    if result and "VOICE_INPUT" in result:
        comando_voz = result.get("VOICE_INPUT", "").strip().lower()
        
        if comando_voz:
            st.info(f"🎤 Se escuchó: *'{comando_voz}'*")
            
            if "abrete sesamo" in comando_voz:
                desbloquear_puerta()
                st.markdown("""
                <div class="alert-success">
                    ✅ ¡ACCESO CONCEDIDO! Palabra clave correcta
                </div>
                """, unsafe_allow_html=True)
            else:
                intento_fallido("Palabra clave incorrecta")
                st.markdown(f"""
                <div class="alert-warning">
                    ❌ Palabra clave incorrecta. Intentos fallidos: {st.session_state.intentos_fallidos}/2
                </div>
                """, unsafe_allow_html=True)
    
    st.divider()
    
    # Botones manuales
    st.write("**Control Manual:**")
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("🔓 Desbloquear"):
            desbloquear_puerta()
            st.rerun()
    
    with col_btn2:
        if st.button("🔐 Bloquear"):
            bloquear_puerta()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# COLUMNA DERECHA - RECONOCIMIENTO FACIAL
# =========================================================
with col_der:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 👤 Desbloqueo por Reconocimiento Facial")
    st.write("Modelo entrenado: Teachable Machine")
    
    st.markdown(f"""
    <div class="status-badge {'status-unlocked' if st.session_state.puerta_abierta else 'status-locked'}">
        {'🔓 ACCESO FACIAL HABILITADO' if not st.session_state.alarma_activa else '🚨 ALARMA ACTIVADA'}
    </div>
    """, unsafe_allow_html=True)
    
    # Capturar foto
    st.write("**Toma una foto para verificación:**")
    foto = st.camera_input("Captura tu rostro")
    
    if foto is not None:
        imagen = Image.open(foto)
        st.image(imagen, caption="Foto capturada", use_container_width=True)
        
        # TODO: Aquí integrar el modelo de Teachable Machine
        st.info("⏳ Analizando rostro... (Integración con Teachable Machine pendiente)")
        
        # Por ahora, simulamos detección
        if st.button("✓ Verificar Rostro"):
            # Esta es una simulación - reemplazar con modelo real
            st.warning("🔄 Implementar modelo Teachable Machine")
    
    else:
        st.markdown("""
        <div style='text-align: center; padding: 40px; color: #64748b;'>
            📷 Esperando captura de cámara...
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ALARMA (Pantalla completa si se activa)
# =========================================================
if st.session_state.alarma_activa:
    st.markdown("""
    <div style='
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, #dc2626, #991b1b);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 999;
        animation: pulse 0.5s infinite;
    '>
        <div style='text-align: center; color: white; font-size: 4em; font-weight: bold;'>
            🚨 ALARMA ACTIVADA 🚨
            <br><br>
            <div style='font-size: 0.5em; margin-top: 20px;'>
                2+ intentos fallidos detectados
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# HISTORIAL DE EVENTOS
# =========================================================
st.divider()
st.markdown("### 📜 Historial de Eventos")

if st.session_state.historial_eventos:
    for evento in st.session_state.historial_eventos[:10]:  # Últimos 10 eventos
        tipo_color = {
            "ÉXITO": "🟢",
            "ERROR": "🔴",
            "ALARMA": "🟠",
            "BLOQUEO": "🟡"
        }.get(evento["tipo"], "⚪")
        
        st.markdown(f"""
        <div class="card" style="margin-bottom: 10px;">
            <small><strong>{tipo_color} [{evento['timestamp']}]</strong> {evento['descripcion']}</small>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("📭 Sin eventos registrados aún")

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer">
    <hr>
    <p>🔐 Smart Door System © 2024 | Sistema de Seguridad Inteligente</p>
    <p>Conectado con Wokwi MQTT | Streamlit + Arduino</p>
</div>
""", unsafe_allow_html=True)
