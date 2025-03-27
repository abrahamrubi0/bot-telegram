#Importacion de librerias
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

#Configuracion del bot
BOT_TOKEN = "8053063957:AAElR1opoRq6tN5GzFC68T5iONeo0K7jJgo" 
BOT_NOMBRE = "Abraham Rubio"  

#Funcion para enviar el mensaje principal y el follow-up
async def send_follow_up(update: Update, text: str):
    await update.message.reply_text(text)
    await update.message.reply_text("¿Necesitas algo más?")

#Comando para iniciar el bot
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_follow_up(update, "¡Hola! Soy un bot de prueba. Envíame 'Hola' o usa /info")

#Comando para obtener informacion del bot
async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_follow_up(update, f"Soy un bot de prueba creado por {BOT_NOMBRE}")

#Comando para sumar dos numeros
async def suma_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        num1 = float(context.args[0])
        num2 = float(context.args[1])
        resultado = num1 + num2
        await send_follow_up(update, f"La suma de {num1} y {num2} es {resultado}")
    except (IndexError, ValueError):
        await send_follow_up(update, "Por favor usa el formato /suma numero1 numero2")

#Comando para restar dos numeros
async def resta_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        num1 = float(context.args[0])
        num2 = float(context.args[1])
        resultado = num1 - num2
        await send_follow_up(update, f"La resta de {num1} y {num2} es {resultado}")
    except (IndexError, ValueError):
        await send_follow_up(update, "Por favor usa el formato /resta numero1 numero2")

#Comando para multiplicar dos numeros
async def multiplicacion_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        num1 = float(context.args[0])
        num2 = float(context.args[1])
        resultado = num1 * num2
        await send_follow_up(update, f"La multiplicación de {num1} y {num2} es {resultado}")
    except (IndexError, ValueError):
        await send_follow_up(update, "Por favor usa el formato /multiplicacion numero1 numero2")

#Comando para dividir dos numeros
async def division_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        num1 = float(context.args[0])
        num2 = float(context.args[1])
        if num2 == 0:
            await send_follow_up(update, "No se puede dividir entre cero")
        else:
            resultado = num1 / num2
            await send_follow_up(update, f"La división de {num1} entre {num2} es {resultado}")
    except (IndexError, ValueError):
        await send_follow_up(update, "Por favor usa el formato /division numero1 numero2")

#Funcion para manejar los mensajes del usuario
#Maneja casos especiales como 'hola' y 'no gracias' en caso de que el usuario no quiera continuar la conversacion
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    if text == 'hola':
        await update.message.reply_text("¡Hola! ¿En qué puedo ayudarte?")
    elif text in ['no gracias', 'no, gracias', 'nada gracias','no']:
        await update.message.reply_text("Gracias por comunicarte, ¡Hasta pronto!")
    else:
        await send_follow_up(update, "No entendí tu mensaje. Prueba con /info para más opciones")

#Funcion para manejar los errores
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

#Funcion para iniciar el bot
if __name__ == '__main__':
    print("Starting bot...")
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Comandos
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("info", info_command))
    app.add_handler(CommandHandler("suma", suma_command))
    app.add_handler(CommandHandler("resta", resta_command))
    app.add_handler(CommandHandler("multiplicacion", multiplicacion_command))
    app.add_handler(CommandHandler("division", division_command))
    
    # Mensajes
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Errores
    app.add_error_handler(error)
    
    print("Ejecutando bot...")
    app.run_polling(poll_interval=3)