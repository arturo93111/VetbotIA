# ==============================
# CARGA DE VARIABLES DE ENTORNO
# ==============================
import os
import csv
import joblib
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

# Cargar modelo de IA entrenado
modelo_intencion = joblib.load("modelo_intencion.pkl")

# ==============================
# MENSAJES NO SOPORTADOS
# ==============================
MENSAJES_NO_SOPORTADOS = [
    "venden",
    "venta",
    "comprar",
    "precio",
    "cuanto cuesta",
    "cuánto cuesta",
    "adopcion",
    "adopción",
    "adoptar",
    "regalan",
    "empleo",
    "trabajo",
    "contratan"
]

# ==============================
# GUARDAR REGISTROS
# ==============================
def guardar_registro(usuario, mensaje, animal, intencion):
    archivo = "registros_bot.csv"

    existe_archivo = os.path.exists(archivo)

    with open(archivo, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not existe_archivo:
            writer.writerow([
                "fecha",
                "usuario",
                "mensaje",
                "animal",
                "intencion"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            usuario,
            mensaje,
            animal,
            intencion
        ])

# ==============================
# DETECCIÓN DE ANIMAL
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
# GENERACIÓN DE RESPUESTA
# ==============================
def generar_respuesta(intencion, animal):

    if intencion == "fuera_alcance":
        return """
Este bot no atiende ese tipo de solicitudes por este medio.

Actualmente solo puede ayudar con:
- Consultas veterinarias básicas
- Urgencias
- Solicitudes de cita

Para otros temas, comunícate directamente con recepción.
"""

    if intencion == "urgencia":
        return """
URGENCIA detectada.

Lleva a tu mascota a una veterinaria 24 horas inmediatamente.

Este bot no sustituye la atención de un médico veterinario.
"""

    elif intencion == "consulta":

        if animal == "perro":
            return """
Consulta detectada para perro.

Recomendación básica:
- Mantén hidratación disponible.
- Observa si hay vómito, diarrea, fiebre o falta de apetito.
- Si los síntomas continúan o empeoran, agenda una cita con un veterinario.

Este bot solo brinda orientación básica.
"""

        elif animal == "gato":
            return """
Consulta detectada para gato.

Recomendación básica:
- Observa si come, toma agua y usa su arenero.
- Los gatos suelen ocultar síntomas.
- Si deja de comer o continúa decaído, agenda una cita veterinaria.

Este bot solo brinda orientación básica.
"""

        elif animal == "conejo":
            return """
Consulta detectada para conejo.

Recomendación básica:
- Los conejos son muy delicados.
- Si deja de comer, está quieto o presenta diarrea, requiere atención veterinaria.
- Manténlo en un ambiente tranquilo mientras agendas una cita.

Este bot solo brinda orientación básica.
"""

        else:
            return """
Detecté una consulta, pero no identifiqué la mascota.

Por favor indica si se trata de:
- perro
- gato
- conejo
"""

    elif intencion == "cita":
        return """
Solicitud de cita detectada.

Para agendar, proporciona:
- Nombre del cliente
- Nombre de la mascota
- Especie
- Motivo de la consulta
- Día preferido
"""

    else:
        return """
No entendí bien tu consulta.

Por favor describe el problema de tu mascota con más detalle.

Ejemplos:
- Mi perro vomita
- Mi gato no come
- Quiero agendar una cita
- Mi conejo no se mueve
"""

# ==============================
# TELEGRAM BOT
# ==============================
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes
)

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = update.message.text
    texto_lower = texto.lower()

    animal = detectar_animal(texto)

    if any(p in texto_lower for p in MENSAJES_NO_SOPORTADOS):
        intencion = "fuera_alcance"
        respuesta = generar_respuesta(intencion, animal)
    else:
        intencion = modelo_intencion.predict([texto])[0]
        respuesta = generar_respuesta(intencion, animal)

    usuario = update.message.from_user.first_name or "desconocido"

    guardar_registro(
        usuario,
        texto,
        animal,
        intencion
    )

    await update.message.reply_text(respuesta)

# ==============================
# FUNCIÓN PRINCIPAL
# ==============================
def main():

    if not TOKEN:
        print("ERROR: No se encontró el TOKEN en el archivo .env")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT, responder)
    )

    print("Bot corriendo con IA entrenada...")
    app.run_polling()

# ==============================
# EJECUCIÓN
# ==============================
if __name__ == "__main__":
    main()