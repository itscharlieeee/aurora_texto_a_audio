import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# Título principal
st.title("De Texto a Voz: Cuentos con Emoción")

# Imagen principal
image = Image.open('aurora.jpg')  # Cambia por tu nueva imagen
st.image(image, width=350)

# Sidebar
with st.sidebar:
    st.subheader("Escribe o selecciona un texto para escucharlo narrado.")
    st.write("Convierte tus palabras o pequeñas historias en voz, "
             "y descubre cómo suena tu imaginación.")

# Carpeta temporal
os.makedirs("temp", exist_ok=True)

# Texto base
st.subheader("Una historia corta: La Luz de Aurora")
st.write(
    "Aurora era una luciérnaga que temía brillar, pensando que su luz era demasiado débil. "
    "Cada noche observaba a las estrellas, deseando ser como ellas. "
    "Una vez, una estrella fugaz descendió y le susurró: "
    "'Tu brillo puede ser pequeño, pero ilumina justo donde otros no pueden llegar.' "
    "Desde entonces, Aurora brilló sin miedo, recordando que la verdadera luz no compite, "
    "solo comparte su camino. ✨"
)

st.markdown("¿Quieres escucharlo? Copia el texto o escribe el tuyo propio 👇")

# Campo de texto
text = st.text_area("Escribe el texto que deseas convertir a audio:")

# Selección de idioma
option_lang = st.selectbox(
    "Selecciona el idioma de la narración:",
    ("Español", "English")
)
lg = 'es' if option_lang == "Español" else 'en'

# Función de conversión
def text_to_speech(text, lg):
    tts = gTTS(text, lang=lg)
    file_name = text[:20] if text else "audio"
    tts.save(f"temp/{file_name}.mp3")
    return file_name

# Botón principal
if st.button("🎧 Convertir a Audio"):
    if text.strip():
        file_name = text_to_speech(text, lg)
        audio_path = f"temp/{file_name}.mp3"
        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
            st.markdown("## Tu narración:")
            st.audio(audio_bytes, format="audio/mp3")

            # Descargar archivo
            b64 = base64.b64encode(audio_bytes).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}.mp3">⬇️ Descargar Audio</a>'
            st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("Por favor, escribe o pega un texto antes de convertirlo.")

# Función de limpieza de archivos
def remove_old_files(days):
    mp3_files = glob.glob("temp/*.mp3")
    now = time.time()
    threshold = now - (days * 86400)
    for f in mp3_files:
        if os.stat(f).st_mtime < threshold:
            os.remove(f)
            print("Archivo eliminado:", f)

remove_old_files(7)
