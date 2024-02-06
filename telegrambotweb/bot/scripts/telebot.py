import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
django.setup()
from bot.models import Comando, Configuracion

import environ
from telegram import error
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

USER_ID_AUTHORIZED_REQUIRE = False

async def showHelp(update):
    help_data = 'Ayuda de los comandos que se pueden utilizar\n'

    for cmd in Comando.objects.all():
        help_data += f'/{cmd.nombre} - {cmd.descripción}\n'
        
    await update.message.reply_text(help_data)
        
        
async def valid_user(user_id):
    result = Configuracion.objects.first().usuario_telegram.filter(usuario_telegram_id=user_id).count() >= 1
    
    return result

async def invalid_user_message(user_id):
    message = 'El usuario actual no está autorizado a usar el bot, consulte al administrador del bot. Tu ID de telegram es: %s' % str(user_id)
    
    return message

async def send_document(document_path, update, context):
    chat_id = update.message.chat_id    
    
    with open(document_path, 'rb') as f:
        await context.bot.send_document(chat_id, f)
        f.close()

async def process_command(command, update, context):
    if Comando.objects.get(nombre=command).documento == None:
        if Comando.objects.get(nombre=command).informacion == None:
            message = f'el comando {command} no tiene ni un documento ni información asociada a él, consulte con el administrador del bot'
        else:
            message = str(Comando.objects.get(nombre=command).informacion.contenido)

        await update.message.reply_text(message)
    else:
        document_path = str(Comando.objects.get(nombre=command).documento.ruta_del_documento)
        
        await send_document(document_path, update, context)
    
    
async def cmd_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global USER_ID_AUTHORIZED_REQUIRE

    command = update.message.text
    
    # removiendo el / del comando
    command = command[1:]
    
    # extrayendo parametros (si es que los hay)
    params = command.split(' ')
    
    # si hay parametros remover el comando de los parametros
    if len(params):
        command = params[0]
        params.pop(0)
    
    # si esta activada la variable de entorno que requiere validacion del id del usuario y el id del usuario
    # se encuentra registrado en la base de datos se da como valido de lo contrario se muestra un mensaje
    if not USER_ID_AUTHORIZED_REQUIRE or await valid_user(update.effective_user.id):
        
        if command == 'ayuda':
            await showHelp(update)
        else:        
            await process_command(command, update, context)
    else:
        message = await invalid_user_message(update.effective_user.id)
        await update.message.reply_text(message)

def run():
    env = environ.Env()
    environ.Env.read_env()
    
    global USER_ID_AUTHORIZED_REQUIRE

    TELEGRAM_BOT_SECRET_KEY = env('TELEGRAM_BOT_SECRET_KEY')
    USER_ID_AUTHORIZED_REQUIRE = env('USER_ID_AUTHORIZED_REQUIRE') == 'True'

    try:
        app = ApplicationBuilder().token(TELEGRAM_BOT_SECRET_KEY).build()
    
        commands = ['ayuda']
        
        for cmd in Comando.objects.all():
            commands.append(cmd.nombre)

        if len(commands) > 1:
            app.add_handler(CommandHandler(commands, cmd_handler))
            app.run_polling()
        else:
            exit('Error no hay comandos en la base de datos, terminando la ejecución el bot...')
    except error.NetworkError:
        print("Error de conexion")
        