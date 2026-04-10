# ==============================
# 🔐 CARGA DE VARIABLES DE ENTORNO
# ==============================
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

# ==============================
# 🧠 DETECCIÓN DE ANIMAL
# ==============================
def detectar_animal(texto):
    texto = texto.lower()

    if any(p in texto for p in ["perro", "cachorro"]):
        return "perro"
    elif any(p in texto for p in ["gato", "gatito"]):
        return "gato"
    elif any(p in texto for p in ["conejo"]):
        return "conejo"
    else:
        return "desconocido"

# ==============================
# 🧠 DETECCIÓN DE INTENCIÓN
# ==============================
def detectar_intencion(texto):
    texto = texto.lower()

    urgencias = [
        "no respira", "convulsiona", "sangra", "desmayado",
        "no se mueve", "no despierta", "ataque"
    ]

    sintomas = [
        "vomita", "diarrea", "no come", "triste",
        "decaido", "fiebre", "tos", "cojea"
    ]

    citas = ["cita", "agendar", "consulta", "horario"]

    # 🔥 Prioridad: urgencias primero
    if any(p in texto for p in urgencias):
        return "urgencia"
    elif any(p in texto for p in sintomas):
        return "consulta"
    elif any(p in texto for p in citas):
        return "cita"
    else:
        return "desconocido"

# ==============================
# 🤖 GENERACIÓN DE RESPUESTA
# ==============================
def generar_respuesta(intencion, animal):

    if intencion == "urgencia":
        return "🚨 URGENCIA detectada. Lleva a tu mascota a una veterinaria 24 hrs inmediatamente."

    elif intencion == "consulta":

        if animal == "perro":
            return """🐶 Posible problema digestivo.
- Mantén hidratación
- Evita comida pesada
- Si hay vómito constante → veterinario"""

        elif animal == "gato":
            return """🐱 Los gatos ocultan síntomas.
- Observa si come
- Revisa vómitos
- Si continúa → veterinario"""

        elif animal == "conejo":
            return """🐰 Conejos son delicados.
- Si deja de comer → puede ser grave
- Mantén ambiente tranquilo
- Acude a veterinario"""

        else:
            return "⚠️ No identifiqué la mascota. ¿Es perro, gato o conejo?"

    elif intencion == "cita":
        return "📅 Puedes agendar una cita en horario laboral. ¿Qué día te gustaría?"

    else:
        return "No entendí bien tu consulta. Intenta describir mejor el problema."

# ==============================
# 🤖 TELEGRAM BOT
# ==============================
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# 🔹 Función que responde mensajes
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text

    intencion = detectar_intencion(texto)
    animal = detectar_animal(texto)

    respuesta = generar_respuesta(intencion, animal)

    await update.message.reply_text(respuesta)

# 🔹 Función principal
def main():
    if not TOKEN:
        print("❌ ERROR: No se encontró el TOKEN en el archivo .env")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT, responder))

    print("🤖 Bot corriendo...")
    app.run_polling()

# ==============================
# 🚀 EJECUCIÓN
# ==============================
if __name__ == "__main__":
    main()