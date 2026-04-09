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

def detectar_intencion(texto):
    texto = texto.lower()

    urgencias = ["no respira", "convulsiona", "sangra", "desmayado", "no se mueve"]
    sintomas = ["vomita", "diarrea", "no come", "triste", "decaido"]
    citas = ["cita", "agendar", "consulta"]

    if any(p in texto for p in urgencias):
        return "urgencia"
    elif any(p in texto for p in sintomas):
        return "consulta"
    elif any(p in texto for p in citas):
        return "cita"
    else:
        return "desconocido"

def generar_respuesta(intencion):
    if intencion == "urgencia":
        return "🚨 Esto parece una URGENCIA. Lleva a tu mascota a una veterinaria 24 hrs inmediatamente."

    elif intencion == "consulta":
        return "⚠️ Puede ser un problema común. Observa a tu mascota, mantenla hidratada y si persiste, agenda una cita con un veterinario."

    elif intencion == "cita":
        return "📅 Puedes agendar una cita en horario laboral. ¿Deseas que te ayude con eso?"

    else:
        return "No entendí bien tu consulta. Intenta describir el problema de tu mascota."

def generar_respuesta(intencion, animal):

    if intencion == "urgencia":
        return "🚨 URGENCIA detectada. Lleva a tu mascota a una veterinaria 24 hrs inmediatamente."

    elif intencion == "consulta":

        if animal == "perro":
            return "🐶 Tu perro podría tener un problema digestivo. Mantén hidratación y observa si sigue vomitando o con diarrea."

        elif animal == "gato":
            return "🐱 Los gatos suelen ocultar síntomas. Si vomita o no come, obsérvalo de cerca y considera llevarlo al veterinario."

        elif animal == "conejo":
            return "🐰 Los conejos son delicados. Si deja de comer o está quieto, puede ser grave. Requiere atención veterinaria."

        else:
            return "⚠️ No identifiqué el tipo de mascota. ¿Es perro, gato o conejo?"

    elif intencion == "cita":
        return "📅 Puedes agendar una cita en horario laboral. ¿Qué día te gustaría?"

    else:
        return "No entendí bien tu consulta. Intenta describir mejor el problema."

###### funcion_telegram#########

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
    app = ApplicationBuilder().token("8545838369:AAE8FYmB2xUB3Bb9z06gyxbLy19F-ZC2Zp0").build()

    app.add_handler(MessageHandler(filters.TEXT, responder))

    print("Bot corriendo...")
    app.run_polling()

if __name__ == "__main__":
    main()