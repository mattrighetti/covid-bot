#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards.
"""
import logging
import threading
from datetime import datetime
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram.parsemode import ParseMode

from covid_data import get_data

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------------------- KEYBOARDS --------------------------------------------

regions_keyboard = [[InlineKeyboardButton("Dati Italia", callback_data='rItaly')],
                    [InlineKeyboardButton("Abruzzo", callback_data='rAbruzzo'), InlineKeyboardButton("Basilicata", callback_data='rBasilicata')],
                    [InlineKeyboardButton("Calabria", callback_data='rCalabria'), InlineKeyboardButton("Campania", callback_data='rCampania')],
                    [InlineKeyboardButton("Emilia-Romagna", callback_data='rEmilia Romagna'), InlineKeyboardButton("Friuli-Venezia Giulia", callback_data='rFriuli Venezia Giulia')],
                    [InlineKeyboardButton("Lazio", callback_data='rLazio'), InlineKeyboardButton("Liguria", callback_data='rLiguria')],
                    [InlineKeyboardButton("Lombardia", callback_data='rLombardia'), InlineKeyboardButton("Marche", callback_data='rMarche')],
                    [InlineKeyboardButton("Molise", callback_data='rMolise'), InlineKeyboardButton("Piemonte", callback_data='rPiemonte')],
                    [InlineKeyboardButton("Puglia", callback_data='rPuglia'), InlineKeyboardButton("Sardegna", callback_data='rSardegna')],
                    [InlineKeyboardButton("Sicilia", callback_data='rSicilia'), InlineKeyboardButton("Toscana", callback_data='rToscana')],
                    [InlineKeyboardButton("Trentino-Alto Adige", callback_data='rTrentino Alto Adige'), InlineKeyboardButton("Umbria", callback_data='rUmbria')],
                    [InlineKeyboardButton("P.A. Trento", callback_data='rP.A. Trento'), InlineKeyboardButton("P.A. Bolzano", callback_data='rP.A. Bolzano')],
                    [InlineKeyboardButton("Valle d'Aosta", callback_data='rValle d\'Aosta'), InlineKeyboardButton("Veneto", callback_data='rVeneto')]]

what_to_do_next_keyboard = [[InlineKeyboardButton("Cambia regione", callback_data='back')], 
                            [InlineKeyboardButton("Aggiorna dati", callback_data='update_current')]]

# -------------------------------------------- BOT METHODS --------------------------------------------

def start(update, context):
    reply_markup = InlineKeyboardMarkup(regions_keyboard)
    
    text = (
        "COVID-19 Bot Italia\n\n"
        "Questo 🤖 ti fornirà tutti i dati riguardanti i casi di COVID-19 regione per regione"
    )

    update.message.reply_text(text)
    update.message.reply_text("Seleziona la regione", reply_markup=reply_markup)


def cov_data(update, context):
    global data_region, data_italy
    query = update.callback_query
    data = query.data.split('r', 1)[1]
    
    headline = f"*{data}*"
    
    if data == 'Italy':
        source = data_italy
    else:
        source = data_region.get(data)
        
    last_update = source['data']
    ricoverati_con_sintomi = source['ricoverati_con_sintomi']
    terapia_intensiva = source['terapia_intensiva']
    totale_ospedalizzati = source['totale_ospedalizzati']
    isolamento_domiciliare = source['isolamento_domiciliare']
    totale_attualmente_positivi = source['totale_attualmente_positivi']
    nuovi_attualmente_positivi = source['nuovi_attualmente_positivi']
    dimessi_guariti = source['dimessi_guariti']
    deceduti = source['deceduti']
    totale_casi = source['totale_casi']
    tamponi = source['tamponi']
    
    date_string = last_update
    format = "%Y-%m-%d %H:%M:%S"
    date = datetime.strptime(date_string, format)
    last_update = date.strftime("%d %b %Y %H:%M")
        
    text = (
            f"{headline}\n\n"
            f"・ Ricoverati con sintomi: *{ricoverati_con_sintomi}*\n"
            f"・ Terapia intensiva: *{terapia_intensiva}*\n"
            f"・ Totale ospedalizzati: *{totale_ospedalizzati}*\n"
            f"・ Isolamento dom.: *{isolamento_domiciliare}*\n"
            f"・ Totale attualmente positivi: *{totale_attualmente_positivi}*\n"
            f"・ Nuovi attualmente positivi: *{nuovi_attualmente_positivi}*\n"
            f"・ Dimessi guariti: *{dimessi_guariti}*\n"
            f"・ Deceduti: *{deceduti}*\n"
            f"・ Totale casi: *{totale_casi}*\n"
            f"・ Tamponi: *{tamponi}*\n"
            f"\nDati aggiornati {last_update}"
        )
    
    reply_markup = InlineKeyboardMarkup(what_to_do_next_keyboard)
    query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

def back(update, context):
    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(regions_keyboard)
    query.edit_message_text(text="Seleziona la regione", reply_markup=reply_markup)

def update(update, context):
    cov_data(update, context)

def help(update, context):
    update.message.reply_text("Usa il comando /start per usare il bot")

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def update_data():
    global data_region, data_italy, data_province
    data_italy, data_region, data_province = get_data()

def periodically_update_data(hours=2):
    SECONDS = 60
    MINUTES = 60
    WAIT_TIME_HOURS = hours * MINUTES * SECONDS

    ticker = threading.Event()
    while not ticker.wait(WAIT_TIME_HOURS):
        update_data()

def main():
    API_TOKEN = os.environ['TOKEN']
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(API_TOKEN, use_context=True)
    
    region_handler = CallbackQueryHandler(cov_data, pattern='^r')
    back_handler = CallbackQueryHandler(back, pattern='^back$')
    update_handler = CallbackQueryHandler(update, pattern='^update$')
    
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(region_handler)
    updater.dispatcher.add_handler(back_handler)
    updater.dispatcher.add_handler(update_handler)
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(error)
    
    global data_region, data_italy, data_province
    data_italy, data_region, data_province = get_data()
    
    # Start the Bot
    updater.start_polling()
    periodically_update_data(hours=3)

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()