import logging
from typing import Text
from telegram import chat, ForceReply, ChatAction, chataction
from telegram.constants import PARSEMODE_MARKDOWN
from telegram.error import TimedOut
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, ConversationHandler, CommandHandler, conversationhandler, dispatcher, filters
import qrcode
import os
from random import randrange
import mime
import smtplib
import mimetypes
from PIL import Image 
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText



EntrardaQR = 0

def start(update, context):
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hola {user.mention_markdown_v2()}\!, escribe /qr y presiona enter para generar un codigo QR',
        reply_markup=ForceReply(selective=True),
    )

def  GenerarQr(update, context):
    update.message.reply_text('Envía el enlace para generar tu código QR')
    return EntrardaQR


def crearQr(enlace):
    codigos = randrange(20000)
    archivoqr = 'TuCodigo' + str(codigos) + '.jpg'
    img = qrcode.make(enlace)
    img.save(archivoqr)
    print("Se generó un QR con el enlace ",enlace )
    return archivoqr 
    

    

def EnviarQR(archivoqr, chat):
    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=None
    )

    

    chat.send_photo(
        photo=open(archivoqr, 'rb')
    )

    


def EntradaEnlace(update, context):
    enlace = update.message.text
    print("El usuario envió el siguiente enlace: ",enlace)
    archivoqr = crearQr(enlace)
    chat = update.message.chat 
    EnviarQR(archivoqr, chat)
    print(chat)
    ChatFile = open('./Chat'+archivoqr+'.txt', 'w') #Cambiar ruta respecto al pc / o \
    ChatFile.write( str(chat))
    ChatFile.close() 
    Gracias(update, context)
    return ConversationHandler.END
    
    
def Gracias(update, context):
    if(update.message.text.upper().find("GRACIAS")):
        update.message.reply_text("De nada")








if __name__ == '__main__':
    updater = Updater(token="1888277066:AAFv7LNFxtVNcEjQOKsVzU0S-8GJS3U0-zc", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('qr', GenerarQr)

        ],

        states={
            EntrardaQR:[MessageHandler(Filters.text, EntradaEnlace)]
        },

        fallbacks=[]


    ))

    updater.start_polling()
    updater.idle()

    
    print("Bot Activo \n")
