# Importación de librerías (ordenadas y agrupadas)
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# --- Configuración --- #
class BotConfig:
    TOKEN = "8053063957:AAElR1opoRq6tN5GzFC68T5iONeo0K7jJgo"
    OWNER = "Abraham Rubio"

# --- Constantes --- #
HELP_MESSAGE = """
¡Hola! Soy un bot de operaciones matemáticas. Puedes usar estos comandos:
/start - Iniciar el bot
/info - Información del bot
/suma num1 num2 - Sumar dos números
/resta num1 num2 - Restar dos números
/multiplicacion num1 num2 - Multiplicar dos números
/division num1 num2 - Dividir dos números
"""

# --- Funciones de utilidad --- #
async def send_response(update: Update, text: str, follow_up: bool = True) -> None:
    
    #Envía una respuesta al usuario.
    
    await update.message.reply_text(text)
    if follow_up:
        await update.message.reply_text("¿Necesitas algo más?")

# Valida y convierte dos argumentos numéricos.
def validate_numbers(args: list) -> tuple:
    if len(args) < 2:
        raise ValueError("Se requieren dos números")
    
    try:
        num1 = float(args[0])
        num2 = float(args[1])
    except ValueError:
        raise ValueError("Los argumentos deben ser números")
        
    return num1, num2

#  Handlers de comandos #
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #Maneja el comando /start
    await send_response(update, HELP_MESSAGE)

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #Maneja el comando /info
    await send_response(update, f"Bot creado por {BotConfig.OWNER}")

# Maneja comandos matemáticos
async def math_command(update: Update, context: ContextTypes.DEFAULT_TYPE, 
                      operation: str) -> None:

    try:
        num1, num2 = validate_numbers(context.args)
        
        if operation == 'suma':
            result = num1 + num2
            operation_text = "suma"
        elif operation == 'resta':
            result = num1 - num2
            operation_text = "resta"
        elif operation == 'multiplicacion':
            result = num1 * num2
            operation_text = "multiplicación"
        elif operation == 'division':
            if num2 == 0:
                await send_response(update, "Error: No se puede dividir entre cero")
                return
            result = num1 / num2
            operation_text = "división"
            
        response = f"La {operation_text} de {num1} y {num2} es {result:.2f}"
        await send_response(update, response)
        
    except ValueError as e:
        await send_response(update, f"Error: {str(e)}\nFormato: /{operation} num1 num2")

#  Handler de mensajes 
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    text = update.message.text.lower()
    
    responses = {
        'hola': "¡Hola! ¿En qué puedo ayudarte?",
        'no gracias': "Gracias por comunicarte, ¡Hasta pronto!",
        'no, gracias': "Gracias por comunicarte, ¡Hasta pronto!",
        'nada gracias': "Gracias por comunicarte, ¡Hasta pronto!",
        'no': "Gracias por comunicarte, ¡Hasta pronto!"
    }
    
    if text in responses:
        await update.message.reply_text(responses[text])
    else:
        await send_response(update, "No entendí tu mensaje. Prueba con /info para más opciones")

# --- Manejo de errores --- #
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #Registra errores y notifica al usuario
    error_msg = f"Error: {context.error}"
    print(error_msg)
    
    if update and update.message:
        await update.message.reply_text("Ocurrió un error. Por favor intenta nuevamente.")

# --- Inicialización del bot --- #
def setup_application() -> Application:
    app = Application.builder().token(BotConfig.TOKEN).build()  # Crea la aplicación con el token
    
    # Handlers de comandos
    command_handlers = {
        'start': start_command,
        'info': info_command,
        'suma': lambda u, c: math_command(u, c, 'suma'),
        'resta': lambda u, c: math_command(u, c, 'resta'),
        'multiplicacion': lambda u, c: math_command(u, c, 'multiplicacion'),
        'division': lambda u, c: math_command(u, c, 'division')
    }
    
    # Agrega handlers de comandos
    for command, handler in command_handlers.items():
        app.add_handler(CommandHandler(command, handler))
    
    # Handler de mensajes
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Handler de errores
    app.add_error_handler(error_handler)
    
    return app

if __name__ == '__main__':
    print("Iniciando bot...")
    application = setup_application()
    print("Ejecutando bot...")
    app.run_polling(poll_interval=3)
