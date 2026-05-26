


pip install streamlit paho-mqtt bokeh streamlit-bokeh-events tensorflow pillow numpy


dond tendria que instalar esto en un github

Ese comando no se instala “en GitHub” directamente.
Se instala en el entorno donde va a correr tu proyecto de Python (tu computador o el servidor donde despliegues la app). En GitHub normalmente solo guardas el archivo con las dependencias.

Lo correcto sería:

Crear un archivo llamado:

requirements.txt
Dentro pegar esto:

streamlit
paho-mqtt
bokeh
streamlit-bokeh-events
tensorflow
pillow
numpy
Subir ese archivo a tu repositorio de GitHub

Luego, dependiendo de dónde ejecutes el proyecto:

En tu PC:

pip install -r requirements.txt
En Streamlit Community Cloud:
automáticamente detecta el requirements.txt e instala todo.

En Render, Railway o Heroku:
también leen ese archivo automáticamente.

Si quieres, también puedo ayudarte a:

organizar la estructura del repo,

crear el requirements.txt completo,

hacer el app.py,

o mostrarte cómo subir y desplegar la app paso a paso.


AttributeError: module 'numpy' has no attribute 'bool8'

¡Perfecto! 🙌
Entonces era incompatibilidad de versiones con numpy.

Te recomiendo dejar el requirements.txt con versiones fijas para que cuando subas el proyecto a GitHub o lo despliegues en otro lado no vuelva a romperse por actualizaciones automáticas.

Por ejemplo:

streamlit==1.35.0
paho-mqtt==1.6.1
bokeh==3.4.1
streamlit-bokeh-events==0.1.2
tensorflow==2.15.0
pillow==10.3.0
numpy==1.26.4
Y luego:

pip freeze > requirements.txt
si quieres guardar exactamente todo tu entorno actual.


ayudame con los códigos

Claro 👀
Pásame:

el código que tienes,

el error que te aparece,

o explícame qué quieres que haga la app,

y te ayudo a arreglarlo o terminarlo.


necesito que me ayudes con un código de github para una app en streamlit, ya yo tengo el código pero debo modificarle unas cosas y añadirle otras de otro código, entonces dame el paso a paso,


La idea general es hacer un sistema de seguridad para una puerta, la puerta se abre unicamente con la cara del dueño o por control de voz, cuando se abre se alumbra un bombillo verde que está en un wokwi

Perfecto, la mejor forma de hacerlo es trabajar por módulos y unirlos poco a poco.
Tu proyecto realmente tiene 4 partes:

Interfaz en Streamlit

Reconocimiento facial

Control por voz

Comunicación con Wokwi/MQTT para prender el bombillo verde

Te dejo el paso a paso REAL para que no te pierdas.

1. Organiza tu proyecto
Crea una carpeta así:

proyecto-seguridad/
│
├── app.py
├── face_auth.py
├── voice_auth.py
├── mqtt_control.py
├── requirements.txt
├── known_faces/
│   └── dueño.jpg
└── .streamlit/
    └── config.toml
2. Instala las librerías
En terminal:

pip install streamlit face_recognition opencv-python speechrecognition paho-mqtt pillow numpy
Y en requirements.txt:

streamlit
face_recognition
opencv-python
speechrecognition
paho-mqtt
pillow
numpy==1.26.4
3. Código para reconocimiento facial
Archivo:

face_auth.py
Código:

import face_recognition
import cv2

known_image = face_recognition.load_image_file("known_faces/dueño.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

def verify_face():
    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()

    if not ret:
        cap.release()
        return False

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    authorized = False

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces([known_encoding], face_encoding)

        if True in matches:
            authorized = True

    cap.release()

    return authorized
4. Código para reconocimiento de voz
Archivo:

voice_auth.py
Código:

import speech_recognition as sr

def verify_voice():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Habla ahora...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="es-ES")
        print("Dijiste:", text)

        if "abrir puerta" in text.lower():
            return True

    except:
        return False

    return False
5. Código MQTT para Wokwi
Archivo:

mqtt_control.py
Código:

import paho.mqtt.publish as publish

BROKER = "broker.hivemq.com"
TOPIC = "puerta/seguridad"

def open_door():
    publish.single(TOPIC, "ON", hostname=BROKER)
6. Código principal Streamlit
Archivo:

app.py
Código:

import streamlit as st
from face_auth import verify_face
from voice_auth import verify_voice
from mqtt_control import open_door

st.title("Sistema de Seguridad Inteligente")

st.write("La puerta se abrirá con reconocimiento facial o comando de voz.")

if st.button("Verificar rostro"):

    if verify_face():
        st.success("Rostro autorizado")
        open_door()
        st.balloons()
    else:
        st.error("Acceso denegado")

if st.button("Verificar voz"):

    if verify_voice():
        st.success("Comando correcto")
        open_door()
        st.balloons()
    else:
        st.error("Comando incorrecto")
7. Configurar Wokwi
En tu simulación de Wokwi necesitas:

ESP32

LED verde

MQTT

Tu ESP32 debe escuchar el topic:

puerta/seguridad
Cuando reciba "ON":

prende el LED verde

simula apertura de puerta

8. Flujo completo
El flujo final sería:

Usuario → Streamlit
        → reconocimiento facial O voz
        → MQTT
        → Wokwi
        → LED verde encendido
9. Cómo subirlo a GitHub
Crear repo en GitHub

Abrir terminal:

git init
git add .
git commit -m "Primer commit"
git branch -M main
git remote add origin TU_LINK
git push -u origin main
10. Cómo ejecutarlo
En terminal:

streamlit run app.py
Ahora lo importante 👀
Como tú ya tienes códigos, lo siguiente es que me mandes:

el código de Streamlit,

el código de Wokwi,

y el otro código que quieres fusionar,

y te digo EXACTAMENTE:

qué líneas borrar,

cuáles mover,

y cómo unir todo sin romper el proyecto.


es un bombillo rojo para cuando la alarma esté apagada y uno verde para cuando esté encendida, te pregunto, si es con fotos de la persona, deberia entrenar el modelo con teachable machine y de ahí concectarlo al código?, es decir que solo se desactive la alarma con una foto mía

Sí, esa es una muy buena opción 👀
Y para tu proyecto puede quedar muchísimo más fácil que entrenar un modelo complejo desde cero.

Pero hay algo importante:

Si quieres reconocimiento facial real → usa face_recognition

Si quieres algo más tipo clasificación con imágenes → usa Teachable Machine

Para TU caso, Teachable Machine puede ser más sencillo porque:

entrenas con fotos tuyas,

exportas el modelo,

Streamlit lo usa,

y si detecta “Salomé” → desactiva alarma.

Lo que te recomiendo
Hazlo así:

Estados del sistema
🔴 Alarma ACTIVADA
bombillo rojo encendido

puerta bloqueada

🟢 Alarma DESACTIVADA
bombillo verde encendido

puerta abierta

Opción MÁS FÁCIL (recomendada)
Usar Teachable Machine
Entrenas dos clases:

Clase 1 → Salome
Clase 2 → Desconocido
Subes:

muchas fotos tuyas

diferentes ángulos

con luz distinta

Luego exportas el modelo en:

TensorFlow/Keras

Y lo conectas a Python.

Flujo del proyecto
Cámara → Streamlit
        → Modelo Teachable Machine
        → Predicción
            → "Salome" = abrir puerta
            → "Desconocido" = alarma sigue activa
Cómo entrenarlo BIEN
En Teachable Machine:

Clase "Salome"
Sube:

30-50 fotos tuyas

de frente

lado derecho

lado izquierdo

con diferentes expresiones

con y sin gafas si usas

Clase "Desconocido"
Puedes poner:

otras personas

imágenes aleatorias

caras de internet

Exportar modelo
Cuando termines:

Export Model
→ TensorFlow
→ Keras
Te descargará:

keras_model.h5
labels.txt
Luego en Streamlit
Tu app:

toma foto

la pasa al modelo

si eres tú:

apaga alarma

LED rojo OFF

LED verde ON

puerta abierta

MQTT + Wokwi
Topics
casa/alarma
Mensajes
ARMADA
DESARMADA
En el ESP32
Si recibe:

ARMADA
→ rojo ON
→ verde OFF

Si recibe:

DESARMADA
→ rojo OFF
→ verde ON

La gran ventaja de Teachable Machine
NO necesitas:

entrenar redes neuronales manualmente,

datasets complejos,

código difícil de IA.

Solo:

fotos,

exportar,

conectar.

Entonces el plan correcto sería:
Parte IA
✅ Teachable Machine

Parte interfaz
✅ Streamlit

Parte IoT
✅ ESP32 + MQTT + Wokwi

Parte visual
✅ LED rojo/verde

Ahora lo siguiente sería que te ayude con:

el código EXACTO para conectar el modelo .h5 a Streamlit

el código del ESP32 en Wokwi

la lógica MQTT

cómo tomar la foto desde la cámara

cómo hacer que la alarma cambie de color automáticamente

y ahí ya quedaría casi terminado.


tengo entrenado el techable con 2 sueños y quiero que si la cara no es ninguno de esos 2 marque desconocido

Sí, puedes hacerlo 👀
Pero hay un detalle importante con Teachable Machine:

Teachable Machine SIEMPRE intentará clasificar la imagen en una de las clases que entrenaste, aunque no sea ninguna.
Entonces necesitas crear tú misma una lógica de “desconocido”.

Cómo hacerlo correctamente
Supongamos que tus clases son:

Salome
Juan
El modelo devolverá probabilidades, por ejemplo:

Salome = 0.92
Juan = 0.08
o

Salome = 0.40
Juan = 0.35
La clave está en el UMBRAL
Tú decides:

Si ninguna probabilidad supera 80%
→ persona desconocida
Ejemplo REAL
Si sale:

Salome → 95%
✅ abre puerta

Si sale:

Salome → 52%
Juan → 48%
❌ desconocido

Entonces tu lógica sería:
if confidence > 0.80:
    acceso permitido
else:
    desconocido
Esto es EXACTAMENTE lo que necesitas
Porque así:

solo abre con rostros MUY parecidos,

evita falsos positivos,

y cualquier otra cara será “desconocido”.

Lo ideal
Entrena:

Clase 1
Salome
Clase 2
Otro dueño
Y NO hagas una clase “desconocido”.

La detección de desconocido la haces en Python con el porcentaje.

Ejemplo completo
Tu modelo predice:

prediction = [
   ("Salome", 0.45),
   ("Juan", 0.40)
]
Como ninguna supera:

0.80
Entonces:

DESCONOCIDO
Resultado final del sistema
Cara reconocida
🟢 verde ON
🔴 rojo OFF
🚪 puerta abierta

Cara desconocida
🔴 rojo ON
🟢 verde OFF
🚨 alarma activa

Consejo MUY importante
Para que funcione bien:

SÍ debes:
usar MUCHAS fotos

diferentes ángulos

iluminación distinta

fondo distinto

NO debes:
entrenar con pocas fotos

usar siempre la misma pose

Ahora lo siguiente sería ayudarte con:

el código Python que lee el .h5,

la cámara en Streamlit,

y el sistema de porcentajes/desconocido.


sí, el código de github tengo que modificarlo, la idea es que se pueda activar y desactivar de 3 formas, con el rostro, con la voz dando instrucciones y hubdiendo manualmente un botón

Perfecto. Entonces tu proyecto ya tiene una lógica MUY clara y profesional 👀

Objetivo final del sistema
La alarma podrá:

ACTIVARSE / DESACTIVARSE de 3 formas:
1. Reconocimiento facial
si reconoce al dueño → desactiva alarma

2. Reconocimiento de voz
comando:

activar alarma
desactivar alarma
abrir puerta
3. Botón manual
botón físico en Wokwi o botón en Streamlit

Estados del sistema
🔴 Alarma ACTIVADA
LED rojo encendido

puerta cerrada

🟢 Alarma DESACTIVADA
LED verde encendido

puerta abierta

Lo MÁS importante ahora
NO empieces a programar todo desde cero.

Como ya tienes un código de GitHub:

primero se modifica,

luego se integra,

luego se añaden funciones.

El paso a paso CORRECTO
PASO 1 — Identifica qué hace cada código
Necesitas decirme:

Código A
¿Qué hace?
Ejemplo:

cámara

IA

Streamlit

Código B
¿Qué hace?
Ejemplo:

MQTT

ESP32

Wokwi

PASO 2 — Estructura recomendada
Tu proyecto debería quedar así:

app.py
face_recognition.py
voice_control.py
mqtt_control.py
model/
   keras_model.h5
   labels.txt
PASO 3 — Variable GLOBAL de la alarma
Esto será CLAVE.

Necesitas una variable:

alarm_active = True
PASO 4 — Cualquier método puede cambiar el estado
Rostro reconocido
alarm_active = False
Voz correcta
alarm_active = False
Botón manual
alarm_active = not alarm_active
PASO 5 — MQTT envía estado a Wokwi
Si:

alarm_active == True
Enviar:

ARMADA
Si:

alarm_active == False
Enviar:

DESARMADA
PASO 6 — Wokwi controla LEDs
ESP32:

ARMADA
🔴 rojo ON
🟢 verde OFF

DESARMADA
🟢 verde ON
🔴 rojo OFF

Cómo se vería la app
En Streamlit:

[ Verificar rostro ]
[ Verificar voz ]
[ Activar/Desactivar manualmente ]
Y abajo:

Estado actual:
🔴 ACTIVADA
o

🟢 DESACTIVADA
La parte MÁS difícil
La integración.

Y ahí es donde debes hacerlo bien para NO romper el código de GitHub.

Entonces AHORA necesito esto 👇
Mándame:

el código de GitHub,

o el link del repo,

o pega los archivos principales,

y te diré EXACTAMENTE:

qué modificar,

dónde pegar cada cosa,

qué borrar,

cómo unir Teachable Machine + voz + MQTT + Streamlit + Wokwi.


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
 
            st.markdown(f"**Resultado:** {clase} con {confianza*100:.1f}% de confianza")
 
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
 

Tu código está MUY bien estructurado 👀
De hecho ya tienes casi todo el proyecto terminado.
Lo que necesitas ahora son ajustes estratégicos para que funcione EXACTAMENTE como quieres.

Te voy a decir qué debes cambiar y por qué.

PRIMER PROBLEMA IMPORTANTE
Aquí:

st.write("3. Si es desconocido → ALERTA (LED rojo)")
Pero tu modelo actualmente parece tener:

0 dueno
1 desconocido
Y tú me dijiste que realmente entrenaste:

Salome
Otra persona
Entonces NO deberías usar una clase “desconocido”.

LO CORRECTO
Tu modelo debería tener SOLO:

0 salome
1 otro_dueno
Y Python decide si alguien es desconocido usando el porcentaje de confianza.

CAMBIO #1 — labels.txt
Debe quedar así:

0 salome
1 angie
o los nombres reales.

NO:

desconocido
CAMBIO #2 — modificar lógica facial
Busca ESTA parte:

if clase == "dueno" and confianza >= umbral:
y reemplázala COMPLETAMENTE por esto:

dueños_autorizados = ["salome", "angie"]

if clase.lower() in dueños_autorizados and confianza >= umbral:
¿Qué hace esto?
Ahora:

si detecta cualquiera de los dueños

Y supera el umbral

abre puerta.

CAMBIO #3 — detección REAL de desconocidos
Busca TODO este bloque:

else:
    enviar_mqtt("Cierra")
    st.session_state.puerta_abierta = False
    st.session_state.ultimo_resultado_facial = f"🚨 Desconocido detectado ({confianza*100:.1f}%)"
    st.session_state.ultimo_comando = "Intento de acceso denegado"
    st.error(f"🚨 ACCESO DENEGADO — Persona no reconocida. LED rojo encendido.")
Y reemplázalo por:

else:
    enviar_mqtt("Cierra")
    st.session_state.puerta_abierta = False

    st.session_state.ultimo_resultado_facial = (
        f"🚨 Persona desconocida ({confianza*100:.1f}%)"
    )

    st.session_state.ultimo_comando = (
        "Intento de acceso denegado"
    )

    st.error(
        "🚨 ACCESO DENEGADO — Persona no autorizada."
    )
¿Por qué esto es mejor?
Porque ahora:

CASO 1
Salome → 95%
✅ abre

CASO 2
Salome → 45%
❌ desconocido

CASO 3
Angie → 91%
✅ abre

CASO 4
Cualquier otra cara → 50%
❌ desconocido

CAMBIO #4 — agregar botón manual tipo switch
AHORA MISMO tienes:

🟢 ABRIR PUERTA
🔴 CERRAR PUERTA
Pero para una alarma queda más profesional un switch.

BORRA esto:

if st.button("🟢 ABRIR PUERTA"):
hasta:

st.warning("🔴 Puerta cerrada manualmente")
Y reemplázalo por:
modo_manual = st.toggle("Activar / Desactivar alarma")

if modo_manual:

    enviar_mqtt("Abre")

    st.session_state.puerta_abierta = True

    st.session_state.ultimo_comando = (
        "Sistema desactivado manualmente"
    )

    st.success("🟢 Sistema DESACTIVADO")

else:

    enviar_mqtt("Cierra")

    st.session_state.puerta_abierta = False

    st.session_state.ultimo_comando = (
        "Sistema activado manualmente"
    )

    st.warning("🔴 Sistema ACTIVADO")
¿Qué ganas con esto?
Ahora tienes EXACTAMENTE las 3 formas:

1️⃣ Voz
abre la puerta
2️⃣ Rostro
Teachable Machine

3️⃣ Manual
Toggle switch

CAMBIO #5 — hacer el proyecto MÁS profesional
Agrega sonidos de alarma.

Cuando alguien desconocido aparezca:

st.audio("alarma.mp3")
CAMBIO #6 — el MQTT está PERFECTO
Tu ESP32 debe escuchar:

IMIA
Y recibir:

{"gesto":"Abre"}
o

{"gesto":"Cierra"}
Eso YA está muy bien hecho.

CONCLUSIÓN
Tu proyecto ya está:
✅ avanzado
✅ bien estructurado
✅ modular
✅ presentable para universidad/proyecto final.

Solo necesitabas:

lógica correcta de desconocidos,

múltiples dueños,

control manual elegante.

Lo siguiente que te recomiendo
Ahora deberías hacer:

1.
Agregar cámara en tiempo real (video continuo)

2.
Agregar detección automática sin tomar foto

3.
Agregar alarma sonora

4.
Agregar registro:

Hora
Persona detectada
Método usado
Y lo MÁS importante ahora:

Necesitas el código del ESP32 en Wokwi para:

LED rojo

LED verde

MQTT

estados.

Porque sin eso no se verá la integración completa.


espera, mi teachable esta con "dueno" y "dueno2"

Perfecto, entonces NO necesitas cambiar el modelo 👀
Tu estructura está bien.

Tus clases quedarían:

0 dueno
1 dueno2
Y cualquier persona que NO sea una de esas dos se detectará usando el umbral de confianza.

Entonces la lógica correcta es:

QUÉ DEBES MODIFICAR
Busca esta parte:

if clase == "dueno" and confianza >= umbral:
y reemplázala por:

dueños_autorizados = ["dueno", "dueno2"]

if clase.lower() in dueños_autorizados and confianza >= umbral:
¿Qué hace esto?
Ahora:

Si detecta:
dueno
o

dueno2
Y la confianza supera el umbral:

✅ abre puerta
🟢 LED verde
🔓 alarma desactivada

Y si NO supera el umbral
Aunque diga:

dueno → 40%
❌ se considera desconocido.

Eso es EXACTAMENTE lo que necesitas.

MUY IMPORTANTE
NO hagas una clase:

desconocido
Porque:

empeora el modelo,

genera más errores,

y Teachable Machine no maneja bien “desconocido”.

El umbral YA hace eso.

Entonces tu sistema queda:
Método 1 — Rostro
dueno

dueno2

Método 2 — Voz
abre la puerta
cierra la puerta
Método 3 — Manual
Toggle switch o botón.

Te recomiendo también cambiar esto
Busca:

st.write("- **'abre la puerta'** → abre y enciende LED verde")
y agrega:

st.write("- Reconoce clases: dueno y dueno2")
EL FLUJO FINAL YA ESTÁ PERFECTO
Persona → cámara
        → modelo Teachable Machine
        → confianza > 85%
              → abrir
        → confianza < 85%
              → desconocido
El siguiente paso importante
Ahora necesitas:

el código ESP32/Wokwi,

para prender:

rojo = alarma activada

verde = alarma desactivada

y ahí ya quedaría completamente funcional.



// =========================================================
// GUARDIAN VISION — CÓDIGO ESP32 WOKWI
// Cambios respecto al original:
//   1. LED rojo encendido por defecto al arrancar (puerta cerrada)
//   2. Se mantiene topic "IMIA" (igual que antes)
//   3. Payload esperado: {"gesto":"Abre"} o {"gesto":"Cierra"}
//      (Streamlit ya fue actualizado para enviar este formato)
//   4. Pin 18 = LED VERDE (puerta abierta)
//   5. Pin 5  = LED ROJO  (puerta cerrada)
//   6. Servo pin 13: 180° = abierto, 0° = cerrado
// =========================================================

#include <ArduinoJson.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ESP32Servo.h>

const char* ssid        = "Wokwi-GUEST";
const char* password    = "";
const char* mqtt_server = "broker.mqttdashboard.com";

// Pines
const int PIN_LED_VERDE = 18;
const int PIN_LED_ROJO  = 5;
const int PIN_SERVO     = 13;

WiFiClient    espClient;
PubSubClient  client(espClient);
Servo         myservo;

String sr2        = "";
String inputString= "";
char   rec[50];

// =========================================================
// SETUP WIFI
// =========================================================
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando a ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectada");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}

// =========================================================
// CALLBACK — se ejecuta cuando llega un mensaje MQTT
// =========================================================
void callback(char* topic, byte* payload, unsigned int length) {
  sr2 = "";
  for (int i = 0; i < length; i++) {
    rec[i]      = payload[i];
    sr2        += rec[i];
    inputString = sr2;
  }

  char msg2[inputString.length() + 1];
  inputString.toCharArray(msg2, inputString.length() + 1);

  StaticJsonDocument<200> doc2;
  DeserializationError error = deserializeJson(doc2, msg2);

  if (error) {
    Serial.print("JSON error: ");
    Serial.println(error.f_str());
    return;
  }

  // Lee el campo "gesto" del JSON
  String gesto = doc2["gesto"].as<String>();

  Serial.print("Gesto recibido: ");
  Serial.println(gesto);

  // -------------------------------------------------------
  // ABRE: LED verde ON, LED rojo OFF, servo 180°
  // -------------------------------------------------------
  if (gesto == "Abre") {
    digitalWrite(PIN_LED_VERDE, HIGH);
    digitalWrite(PIN_LED_ROJO,  LOW);
    myservo.write(180);
    Serial.println(">> Puerta ABIERTA");
  }

  // -------------------------------------------------------
  // CIERRA: LED rojo ON, LED verde OFF, servo 0°
  // -------------------------------------------------------
  else if (gesto == "Cierra") {
    digitalWrite(PIN_LED_ROJO,  HIGH);
    digitalWrite(PIN_LED_VERDE, LOW);
    myservo.write(0);
    Serial.println(">> Puerta CERRADA");
  }
}

// =========================================================
// RECONEXIÓN MQTT
// =========================================================
void reconnect() {
  while (!client.connected()) {
    Serial.print("Conectando MQTT...");
    if (client.connect("CerraduraIA")) {
      Serial.println("conectado");
      client.subscribe("IMIA");   // topic principal — igual que Streamlit
    } else {
      Serial.print("falla rc=");
      Serial.print(client.state());
      Serial.println(" — reintentando en 5s");
      delay(5000);
    }
  }
}

// =========================================================
// SETUP
// =========================================================
void setup() {
  Serial.begin(115200);

  pinMode(PIN_LED_VERDE, OUTPUT);
  pinMode(PIN_LED_ROJO,  OUTPUT);

  // Estado inicial: puerta cerrada = LED rojo encendido
  digitalWrite(PIN_LED_VERDE, LOW);
  digitalWrite(PIN_LED_ROJO,  HIGH);

  myservo.setPeriodHertz(50);
  myservo.attach(PIN_SERVO, 500, 2400);
  myservo.write(0);   // posición cerrado al inicio

  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

// =========================================================
// LOOP
// =========================================================
void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}

Perfecto 👀
Tu integración ya está MUY bien hecha.
De verdad ya tienes un proyecto bastante completo.

Tu ESP32:
✅ recibe MQTT
✅ controla LEDs
✅ mueve servo
✅ tiene estado inicial correcto
✅ está sincronizado con Streamlit.

Ahora te voy a decir SOLO los cambios importantes que faltan para dejarlo MUCHO más sólido y profesional.

1. PROBLEMA IMPORTANTE EN TU CALLBACK
Aquí:

for (int i = 0; i < length; i++) {
estás llenando rec[i] pero nunca cierras el string.

Entonces a veces el JSON puede romperse.

SOLUCIÓN
Reemplaza TODO esto:

sr2 = "";
for (int i = 0; i < length; i++) {
  rec[i]      = payload[i];
  sr2        += rec[i];
  inputString = sr2;
}
por esto:

String mensaje = "";

for (int i = 0; i < length; i++) {
  mensaje += (char)payload[i];
}
Y reemplaza esto:
char msg2[inputString.length() + 1];
inputString.toCharArray(msg2, inputString.length() + 1);
por:

char msg2[mensaje.length() + 1];
mensaje.toCharArray(msg2, mensaje.length() + 1);
¿Por qué?
Porque:

es más limpio,

más seguro,

evita errores JSON,

y elimina variables innecesarias.

2. AGREGA UNA ALARMA SONORA 🚨
Esto le da MUCHÍSIMO nivel al proyecto.

En Wokwi agrega:
Buzzer
Pin recomendado:

const int PIN_BUZZER = 19;
En setup()
Agrega:

pinMode(PIN_BUZZER, OUTPUT);
Cuando detecte desconocido
Ahora mismo Streamlit manda:

{"gesto":"Cierra"}
pero eso también ocurre cuando cierras normalmente.

Entonces necesitamos DIFERENCIAR:

Cierre normal
{"gesto":"Cierra"}
Intruso
{"gesto":"Alarma"}
3. MODIFICA STREAMLIT
Busca:

enviar_mqtt("Cierra")
en la parte de desconocidos.

Y cambia SOLO esa por:

enviar_mqtt("Alarma")
4. AGREGA ESTO EN EL ESP32
Debajo de:

else if (gesto == "Cierra")
agrega:

else if (gesto == "Alarma") {

  digitalWrite(PIN_LED_ROJO, HIGH);
  digitalWrite(PIN_LED_VERDE, LOW);

  myservo.write(0);

  for (int i = 0; i < 5; i++) {

    tone(PIN_BUZZER, 1000);
    delay(300);

    noTone(PIN_BUZZER);
    delay(300);
  }

  Serial.println(">> ALERTA DE INTRUSO");
}
¿Qué pasa ahora?
Dueño reconocido
🟢 verde
🔓 abre
😌 silencioso

Cierre manual
🔴 rojo
🔒 cerrado

Intruso
🚨 buzzer
🔴 rojo
🔒 bloqueado

5. AGREGA LOGS EN STREAMLIT
Esto le da MUCHÍSIMA presentación.

Arriba:

from datetime import datetime
Session state
Agrega:

if "logs" not in st.session_state:
    st.session_state.logs = []
Cuando abras o cierres
Ejemplo:

st.session_state.logs.append(
    f"{datetime.now().strftime('%H:%M:%S')} - Dueño reconocido"
)
Y abajo del todo:
st.markdown("## 📋 Historial")

for log in reversed(st.session_state.logs[-10:]):
    st.write(log)
6. TE RECOMIENDO ESTO PARA EL MODELO
Sube MUCHAS fotos:

cerca

lejos

luz blanca

luz amarilla

con gafas

sin gafas

Porque Teachable Machine se confunde MUCHO con poca data.

7. TU FLUJO FINAL YA QUEDA PROFESIONAL
Cámara/Voz/Botón
        ↓
Streamlit
        ↓
Teachable Machine
        ↓
MQTT
        ↓
ESP32 Wokwi
        ↓
Servo + LEDs + Buzzer
Honestamente, ya tienes:
✅ IA
✅ IoT
✅ visión artificial
✅ MQTT
✅ interfaz multimodal
✅ automatización
✅ seguridad inteligente

Es un MUY buen proyecto para Interfaces Multimodales.


listo, dame los codigos exactos para que solo sea copiar y pegar en github y en wokwi

1. ARCHIVO app.py (STREAMLIT)
Copia TODO este código completo en tu archivo:

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
2. ARCHIVO requirements.txt
streamlit
paho-mqtt
bokeh
streamlit-bokeh-events
tensorflow
pillow
numpy==1.26.4
3. ARCHIVO labels.txt
0 dueno
1 dueno2
4. WOKWI — CÓDIGO ESP32
Pega TODO esto en Wokwi:

#include <ArduinoJson.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ESP32Servo.h>

const char* ssid = "Wokwi-GUEST";
const char* password = "";
const char* mqtt_server = "broker.mqttdashboard.com";

const int PIN_LED_VERDE = 18;
const int PIN_LED_ROJO = 5;
const int PIN_SERVO = 13;
const int PIN_BUZZER = 19;

WiFiClient espClient;
PubSubClient client(espClient);

Servo myservo;

void setup_wifi() {

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

void callback(char* topic, byte* payload, unsigned int length) {

  String mensaje = "";

  for (int i = 0; i < length; i++) {
    mensaje += (char)payload[i];
  }

  char msg[mensaje.length() + 1];

  mensaje.toCharArray(msg, mensaje.length() + 1);

  StaticJsonDocument<200> doc;

  deserializeJson(doc, msg);

  String gesto = doc["gesto"];

  if (gesto == "Abre") {

    digitalWrite(PIN_LED_VERDE, HIGH);
    digitalWrite(PIN_LED_ROJO, LOW);

    myservo.write(180);

  }

  else if (gesto == "Cierra") {

    digitalWrite(PIN_LED_ROJO, HIGH);
    digitalWrite(PIN_LED_VERDE, LOW);

    myservo.write(0);

  }

  else if (gesto == "Alarma") {

    digitalWrite(PIN_LED_ROJO, HIGH);
    digitalWrite(PIN_LED_VERDE, LOW);

    myservo.write(0);

    for (int i = 0; i < 5; i++) {

      tone(PIN_BUZZER, 1000);

      delay(300);

      noTone(PIN_BUZZER);

      delay(300);
    }
  }
}

void reconnect() {

  while (!client.connected()) {

    if (client.connect("GuardianVision")) {

      client.subscribe("IMIA");

    } else {

      delay(5000);
    }
  }
}

void setup() {

  Serial.begin(115200);

  pinMode(PIN_LED_VERDE, OUTPUT);
  pinMode(PIN_LED_ROJO, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);

  digitalWrite(PIN_LED_ROJO, HIGH);

  myservo.setPeriodHertz(50);

  myservo.attach(PIN_SERVO, 500, 2400);

  myservo.write(0);

  setup_wifi();

  client.setServer(mqtt_server, 1883);

  client.setCallback(callback);
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }

  client.loop();
}
5. EJECUTAR EL PROYECTO
En terminal:

streamlit run app.py
6. ARCHIVOS QUE DEBEN ESTAR EN LA MISMA CARPETA
app.py
requirements.txt
keras_model.h5
labels.txt
7. COMPONENTES EN WOKWI
Conecta:

LED verde → pin 18

LED rojo → pin 5

Servo → pin 13

Buzzer → pin 19

8. RESULTADO FINAL
Voz
🎤 “abre la puerta”

→ abre servo
→ LED verde

Rostro reconocido
→ puerta abierta

Intruso
→ LED rojo
→ buzzer
→ puerta cerrada

Manual
→ toggle switch en Streamlit


TypeError: Error when deserializing class 'DepthwiseConv2D' using 

config={'name': 'expanded_conv_depthwise', 'trainable': True, 'dtype': 

'float32', 'kernel_size': [3, 3], 'strides': [1, 1], 'padding': 'same', 

'data_format': 'channels_last', 'dilation_rate': [1, 1], 'groups': 1, 

'activation': 'linear', 'use_bias': False, 'bias_initializer': {'class_name': 

'Zeros', 'config': {}}, 'bias_regularizer': None, 'activity_regularizer': None, 

'bias_constraint': None, 'depth_multiplier': 1, 'depthwise_initializer': 

{'class_name': 'VarianceScaling', 'config': {'scale': 1, 'mode': 'fan_avg', 

'distribution': 'uniform', 'seed': None}}, 'depthwise_regularizer': None, 

'depthwise_constraint': None}.


Exception encountered: Unrecognized keyword arguments passed to DepthwiseConv2D:

{'groups': 1}

Ese error pasa porque el modelo de Teachable Machine fue creado con una versión MÁS NUEVA de TensorFlow que la que tienes instalada.

El problema es este:

'groups': 1
Tu TensorFlow actual no reconoce ese parámetro en DepthwiseConv2D.

SOLUCIÓN (la correcta)
Debes actualizar TensorFlow.

1. BORRA el TensorFlow viejo
En terminal:

pip uninstall tensorflow
Si pregunta:

Proceed (Y/n)?
pon:

y
2. INSTALA esta versión EXACTA
pip install tensorflow==2.15.0
3. CAMBIA TU requirements.txt
Déjalo así EXACTAMENTE:

streamlit
paho-mqtt
bokeh
streamlit-bokeh-events
tensorflow==2.15.0
pillow
numpy==1.26.4
¿Por qué pasa esto?
Teachable Machine actualmente exporta modelos compatibles con TensorFlow moderno.

Y seguramente tienes:

TensorFlow muy viejo
o

Keras incompatible.

IMPORTANTE
NO instales:

keras
por separado.

TensorFlow ya trae Keras integrado.

DESPUÉS DE INSTALAR
Vuelve a correr:

streamlit run app.py
Si el error sigue
Entonces tu modelo fue exportado con:

TensorFlow.js
y NO con:

TensorFlow > Keras
En ese caso:

vuelve a exportar así:
Export Model
→ TensorFlow
→ Keras
y reemplaza:

keras_model.h5

labels.txt

Lo MÁS probable
✅ solo necesitas:

pip install tensorflow==2.15.0
y queda funcionando.


la app está mal

¿Qué está pasando exactamente? 👀
Necesito que me mandes una de estas cosas:

el error que aparece,

una captura,

o decirme qué parte no funciona.

Por ejemplo:

¿no abre Streamlit?

¿no reconoce la cara?

¿no funciona el micrófono?

¿Wokwi no prende LEDs?

¿el servo no gira?

¿MQTT no conecta?

¿la cámara no abre?

¿la app se ve dañada visualmente?

Con eso te digo EXACTAMENTE qué línea corregir.


mira el codigo original, quiero que este igualito solo añadele lo de teachable machine y la conexion con wokwi. # =========================================================
# GUARDIAN VISION - CÓDIGO COMPLETO CON VOZ CORREGIDA
# =========================================================

import streamlit as st
import paho.mqtt.client as mqtt
import json
from PIL import Image
from bokeh.models import Button, CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

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
# LAYOUT
# =========================================================
col1, col2 = st.columns([1, 2])

# =========================================================
# PANEL IZQUIERDO
# =========================================================
with col1:

    # ESTADO
    if st.session_state.alarma_activa:
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
    # PROCESAR VOZ CORREGIDO
    # =====================================================
    if result:
        st.write("DEBUG RESULTADO:", result)

        if "GET_TEXT" in result:
            comando = result.get("GET_TEXT", "").strip().lower()

            st.session_state.ultimo_comando = comando

            st.success(f"🎤 Se escuchó: {comando}")

            if (
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
                enviar_mqtt("desactivado")
                st.warning("🔴 Alarma DESACTIVADA")

            else:
                st.error("⚠️ Comando no reconocido. Intenta de nuevo.")

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
# PANEL DERECHO - CÁMARA
# =========================================================
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("<h2 style='color:black;'>📸 Cámara de Vigilancia</h2>", unsafe_allow_html=True)

    foto = st.camera_input("Toma una captura de seguridad")

    if foto is not None:
        imagen = Image.open(foto)

        st.image(imagen, caption="Captura actual", use_container_width=True)

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
    "<p style='color:black; text-align:center;'>Guardian Vision © Proyecto Interfaces Multimodales | Angie Vargas - Isabella Saldarriaga - Salome Rivero</p>",
    unsafe_allow_html=True
)

Perfecto, ahora sí entendí EXACTAMENTE lo que necesitas 👀

NO quieres cambiar la interfaz ni la lógica original.
Solo quieres:

✅ mantener el diseño EXACTO
✅ mantener voz EXACTA
✅ mantener botones EXACTOS
✅ mantener estructura EXACTA

y SOLO añadir:

Teachable Machine

conexión correcta con Wokwi.

Entonces SOLO debes agregar estas partes.

1. AGREGA ESTOS IMPORTS
Debajo de:

from PIL import Image
agrega:

import numpy as np
import tensorflow as tf
2. CAMBIA EL TOPIC MQTT
Busca:

TOPIC = "voice_ctrl"
y reemplázalo por:

TOPIC = "IMIA"
Porque Wokwi escucha "IMIA".

3. CAMBIA LA FUNCIÓN MQTT
BORRA esta función:

def enviar_mqtt(mensaje):
    try:
        payload = json.dumps({"Act1": mensaje})
        mqtt_client.publish(TOPIC, payload)
    except:
        pass
Y reemplázala por ESTA:
def enviar_mqtt(mensaje):

    try:

        payload = json.dumps({
            "gesto": mensaje
        })

        mqtt_client.publish(TOPIC, payload)

    except:
        pass
4. AGREGA EL MODELO TEACHABLE MACHINE
Debajo de:

mqtt_client = setup_mqtt()
agrega TODO esto:

# =========================================================
# MODELO TEACHABLE MACHINE
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
5. CAMBIA LOS MENSAJES MQTT
BUSCA:
enviar_mqtt("activado")
y reemplázalo por:

enviar_mqtt("Abre")
BUSCA:
enviar_mqtt("desactivado")
y reemplázalo por:

enviar_mqtt("Cierra")
6. AGREGA TEACHABLE MACHINE A LA CÁMARA
Busca TODO este bloque:

if foto is not None:
    imagen = Image.open(foto)

    st.image(imagen, caption="Captura actual", use_container_width=True)

    if st.session_state.alarma_activa:
        st.error("🚨 ALERTA: Presencia detectada")
        enviar_mqtt("intruso")
    else:
        st.success("✅ Monitoreo realizado (alarma apagada)")
Y reemplázalo COMPLETO por esto:
if foto is not None:

    imagen = Image.open(foto)

    st.image(imagen, caption="Captura actual", use_container_width=True)

    clase, confianza = clasificar_imagen(imagen)

    st.write(f"Clase detectada: {clase}")

    st.write(f"Confianza: {confianza*100:.1f}%")

    dueños = ["dueno", "dueno2"]

    umbral = 0.85

    if clase.lower() in dueños and confianza >= umbral:

        st.success("✅ Dueño reconocido")

        st.session_state.alarma_activa = False

        enviar_mqtt("Abre")

    else:

        st.error("🚨 PERSONA DESCONOCIDA")

        st.session_state.alarma_activa = True

        enviar_mqtt("Alarma")
7. CAMBIA EL TEXTO DEL SIDEBAR
Busca:

st.write("Toma una foto para monitorear.")
st.write("Si la alarma está activa, enviará alerta MQTT.")
Y reemplázalo por:
st.write("Toma una foto para reconocimiento facial.")
st.write("Si reconoce al dueño → desactiva alarma.")
st.write("Si detecta desconocido → activa alarma.")
8. ARCHIVOS NECESARIOS
En la misma carpeta:

app.py
keras_model.h5
labels.txt
9. labels.txt
0 dueno
1 dueno2
10. requirements.txt
streamlit
paho-mqtt
bokeh
streamlit-bokeh-events
tensorflow==2.15.0
pillow
numpy==1.26.4
RESULTADO FINAL
Tu app original queda EXACTAMENTE igual 👀

Pero ahora:

voz controla Wokwi,

botones controlan Wokwi,

cámara usa Teachable Machine,

si eres tú → desactiva alarma,

si no → activa alarma + LED rojo.


no me digas ccambio de parte por parte, solo modificame el codigo que te acabo de enviar para pegarlo tal cual

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
    st.write("- enciende la alarma")
    st.write("- apaga la alarma")

    st.write("### 🔘 Control Manual")
    st.write("- Botón ENCENDER")
    st.write("- Botón APAGAR")

    st.write("### 📸 Reconocimiento Facial")
    st.write("Clases permitidas:")
    st.code("dueno\ndueno2")

# =========================================================
# MQTT
# =========================================================
BROKER = "broker.mqttdashboard.com"
PORT = 1883
TOPIC = "IMIA"

@st.cache_resource
def setup_mqtt():

    client = mqtt.Client(client_id="ANGIE_GUARD")

    try:
        client.connect(BROKER, PORT, 60)
    except:
        pass

    return client

mqtt_client = setup_mqtt()

# =========================================================
# MODELO TEACHABLE MACHINE
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
if "alarma_activa" not in st.session_state:
    st.session_state.alarma_activa = False

if "ultimo_comando" not in st.session_state:
    st.session_state.ultimo_comando = "Sin comandos aún"

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
# LAYOUT
# =========================================================
col1, col2 = st.columns([1, 2])

# =========================================================
# PANEL IZQUIERDO
# =========================================================
with col1:

    if st.session_state.alarma_activa:
        panel_bg = "#dcfce7"
        panel_border = "#16a34a"
        panel_text = "#166534"
        estado_texto = "🟢 ALARMA ACTIVADA"

    else:
        panel_bg = "#fee2e2"
        panel_border = "#dc2626"
        panel_text = "#991b1b"
        estado_texto = "🔴 ALARMA DESACTIVADA"

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
    # PROCESAR VOZ
    # =====================================================
    if result:

        if "GET_TEXT" in result:

            comando = result.get("GET_TEXT", "").strip().lower()

            st.session_state.ultimo_comando = comando

            st.success(f"🎤 Se escuchó: {comando}")

            if (
                "enciende la alarma" in comando or
                "activar alarma" in comando or
                "enciende alarma" in comando or
                "activar" in comando or
                "encender" in comando
            ):

                st.session_state.alarma_activa = True

                enviar_mqtt("Cierra")

                st.success("🟢 Alarma ACTIVADA")

            elif (
                "apaga la alarma" in comando or
                "desactiva la alarma" in comando or
                "apaga alarma" in comando or
                "desactivar" in comando or
                "apagar" in comando
            ):

                st.session_state.alarma_activa = False

                enviar_mqtt("Abre")

                st.warning("🔴 Alarma DESACTIVADA")

            else:

                st.error("⚠️ Comando no reconocido")

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

        enviar_mqtt("Cierra")

    if st.button("🔴 APAGAR ALARMA"):

        st.session_state.alarma_activa = False

        st.session_state.ultimo_comando = "Apagado manual"

        enviar_mqtt("Abre")

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
        <h2 style="color:{panel_text};">{estado_texto}</h2>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# PANEL DERECHO
# =========================================================
with col2:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("<h2 style='color:black;'>📸 Cámara de Vigilancia</h2>", unsafe_allow_html=True)

    foto = st.camera_input("Toma una captura de seguridad")

    if foto is not None:

        imagen = Image.open(foto)

        st.image(imagen, caption="Captura actual", use_container_width=True)

        clase, confianza = clasificar_imagen(imagen)

        st.write(f"Clase detectada: {clase}")

        st.write(f"Confianza: {confianza*100:.1f}%")

        dueños = ["dueno", "dueno2"]

        umbral = 0.85

        if clase.lower() in dueños and confianza >= umbral:

            st.success("✅ Dueño reconocido")

            st.session_state.alarma_activa = False

            enviar_mqtt("Abre")

        else:

            st.error("🚨 PERSONA DESCONOCIDA")

            st.session_state.alarma_activa = True

            enviar_mqtt("Alarma")

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
    "<p style='color:black; text-align:center;'>Guardian Vision © Proyecto Interfaces Multimodales | Angie Vargas - Isabella Saldarriaga - Salome Rivero</p>",
    unsafe_allow_html=True
)

y en la parte de reconocimiento facial, hazlo porcentual, si el valor de reconocimiento es menor al 40% para dueno o dueno2, la puerta no se abre, marca "desconocido"

# REEMPLAZA SOLO ESTA PARTE:

if foto is not None:

    imagen = Image.open(foto)

    st.image(imagen, caption="Captura actual", use_container_width=True)

    clase, confianza = clasificar_imagen(imagen)

    porcentaje = confianza * 100

    st.write(f"Clase detectada: {clase}")

    st.write(f"Confianza: {porcentaje:.1f}%")

    dueños = ["dueno", "dueno2"]

    # =====================================================
    # SI LA CONFIANZA ES MENOR A 40%
    # SE CONSIDERA DESCONOCIDO
    # =====================================================

    if porcentaje < 40:

        st.error("🚨 PERSONA DESCONOCIDA")

        st.write("Confianza demasiado baja para reconocer al dueño.")

        st.session_state.alarma_activa = True

        enviar_mqtt("Alarma")

    # =====================================================
    # DUEÑO RECONOCIDO
    # =====================================================

    elif clase.lower() in dueños:

        st.success("✅ Dueño reconocido")

        st.write(f"Acceso permitido ({porcentaje:.1f}%)")

        st.session_state.alarma_activa = False

        enviar_mqtt("Abre")

    # =====================================================
    # DESCONOCIDO
    # =====================================================

    else:

        st.error("🚨 PERSONA DESCONOCIDA")

        st.write(f"Acceso denegado ({porcentaje:.1f}%)")

        st.session_state.alarma_activa = True

        enviar_mqtt("Alarma")

dame el código completo con eso

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
    st.write("- enciende la alarma")
    st.write("- apaga la alarma")

    st.write("### 🔘 Control Manual")
    st.write("- Botón ENCENDER")
    st.write("- Botón APAGAR")

    st.write("### 📸 Reconocimiento Facial")
    st.write("Clases permitidas:")
    st.code("dueno\ndueno2")

# =========================================================
# MQTT
# =========================================================
BROKER = "broker.mqttdashboard.com"
PORT = 1883
TOPIC = "IMIA"

@st.cache_resource
def setup_mqtt():

    client = mqtt.Client(client_id="ANGIE_GUARD")

    try:
        client.connect(BROKER, PORT, 60)
    except:
        pass

    return client

mqtt_client = setup_mqtt()

# =========================================================
# MODELO TEACHABLE MACHINE
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
if "alarma_activa" not in st.session_state:
    st.session_state.alarma_activa = False

if "ultimo_comando" not in st.session_state:
    st.session_state.ultimo_comando = "Sin comandos aún"

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
# LAYOUT
# =========================================================
col1, col2 = st.columns([1, 2])

# =========================================================
# PANEL IZQUIERDO
# =========================================================
with col1:

    if st.session_state.alarma_activa:
        panel_bg = "#dcfce7"
        panel_border = "#16a34a"
        panel_text = "#166534"
        estado_texto = "🟢 ALARMA ACTIVADA"

    else:
        panel_bg = "#fee2e2"
        panel_border = "#dc2626"
        panel_text = "#991b1b"
        estado_texto = "🔴 ALARMA DESACTIVADA"

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
    # PROCESAR VOZ
    # =====================================================
    if result:

        if "GET_TEXT" in result:

            comando = result.get("GET_TEXT", "").strip().lower()

            st.session_state.ultimo_comando = comando

            st.success(f"🎤 Se escuchó: {comando}")

            if (
                "enciende la alarma" in comando or
                "activar alarma" in comando or
                "enciende alarma" in comando or
                "activar" in comando or
                "encender" in comando
            ):

                st.session_state.alarma_activa = True

                enviar_mqtt("Cierra")

                st.success("🟢 Alarma ACTIVADA")

            elif (
                "apaga la alarma" in comando or
                "desactiva la alarma" in comando or
                "apaga alarma" in comando or
                "desactivar" in comando or
                "apagar" in comando
            ):

                st.session_state.alarma_activa = False

                enviar_mqtt("Abre")

                st.warning("🔴 Alarma DESACTIVADA")

            else:

                st.error("⚠️ Comando no reconocido")

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

        enviar_mqtt("Cierra")

    if st.button("🔴 APAGAR ALARMA"):

        st.session_state.alarma_activa = False

        st.session_state.ultimo_comando = "Apagado manual"

        enviar_mqtt("Abre")

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
        <h2 style="color:{panel_text};">{estado_texto}</h2>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# PANEL DERECHO
# =========================================================
with col2:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("<h2 style='color:black;'>📸 Cámara de Vigilancia</h2>", unsafe_allow_html=True)

    foto = st.camera_input("Toma una captura de seguridad")

    if foto is not None:

        imagen = Image.open(foto)

        st.image(imagen, caption="Captura actual", use_container_width=True)

        clase, confianza = clasificar_imagen(imagen)

        porcentaje = confianza * 100

        st.write(f"Clase detectada: {clase}")

        st.write(f"Confianza: {porcentaje:.1f}%")

        dueños = ["dueno", "dueno2"]

        # =====================================================
        # SI LA CONFIANZA ES MENOR A 40%
        # SE CONSIDERA DESCONOCIDO
        # =====================================================
        if porcentaje < 40:

            st.error("🚨 PERSONA DESCONOCIDA")

            st.write("Confianza demasiado baja para reconocer al dueño.")

            st.session_state.alarma_activa = True

            enviar_mqtt("Alarma")

        # =====================================================
        # DUEÑO RECONOCIDO
        # =====================================================
        elif clase.lower() in dueños:

            st.success("✅ Dueño reconocido")

            st.write(f"Acceso permitido ({porcentaje:.1f}%)")

            st.session_state.alarma_activa = False

            enviar_mqtt("Abre")

        # =====================================================
        # DESCONOCIDO
        # =====================================================
        else:

            st.error("🚨 PERSONA DESCONOCIDA")

            st.write(f"Acceso denegado ({porcentaje:.1f}%)")

            st.session_state.alarma_activa = True

            enviar_mqtt("Alarma")

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
    "<p style='color:black; text-align:center;'>Guardian Vision © Proyecto Interfaces Multimodales | Angie Vargas - Isabella Saldarriaga - Salome Rivero</p>",
    unsafe_allow_html=True
)

