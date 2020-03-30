const Telegraf = require('telegraf')
const { Markup } = require('telegraf')
const axios = require('axios')
const extra = require('telegraf/extra')

const bot = new Telegraf(process.env.BOT_TOKEN)

const mainMenu = Markup.inlineKeyboard([
    [Markup.callbackButton("Dati Italia", 'nItaly')],
    [Markup.callbackButton("Abruzzo", 'rAbruzzo'), Markup.callbackButton("Basilicata", 'rBasilicata')],
    [Markup.callbackButton("Calabria", 'rCalabria'), Markup.callbackButton("Campania", 'rCampania')],
    [Markup.callbackButton("Emilia-Romagna", 'rEmilia Romagna'), Markup.callbackButton("Friuli-Venezia Giulia", 'rFriuli Venezia Giulia')],
    [Markup.callbackButton("Lazio", 'rLazio'), Markup.callbackButton("Liguria", 'rLiguria')],
    [Markup.callbackButton("Lombardia", 'rLombardia'), Markup.callbackButton("Marche", 'rMarche')],
    [Markup.callbackButton("Molise", 'rMolise'), Markup.callbackButton("Piemonte", 'rPiemonte')],
    [Markup.callbackButton("Puglia", 'rPuglia'), Markup.callbackButton("Sardegna", 'rSardegna')],
    [Markup.callbackButton("Sicilia", 'rSicilia'), Markup.callbackButton("Toscana", 'rToscana')],
    [Markup.callbackButton("P.A. Trento", 'rP.A. Trento'), Markup.callbackButton("Umbria", 'rUmbria')],
    [Markup.callbackButton("Valle d'Aosta", 'rValle d\'Aosta'), Markup.callbackButton("P.A. Bolzano", 'rP.A. Bolzano')],
    [Markup.callbackButton("Veneto", 'rVeneto')]
])

const region_data_url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni-latest.json'
const province_data_url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province-latest.json'
const italy_data_url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale-latest.json'

const regionMenu = Markup.inlineKeyboard([Markup.callbackButton("Cambia regione", 'back')])

var regions_data, italy_data = {}

function updateRegionsData() {
    var timeout = 1000 * 60 * 60 * 1
    console.log("Getting regions data")
    axios.get(region_data_url).then(res => {
        regions_data = res.data
    }).catch(() => {
        timeout = 1000 * 60 * 2
    })

    setInterval(updateRegionsData, timeout)
}

function updateItalyData() {
    var timeout = 1000 * 60 * 60 * 1
    console.log("Getting data")

    axios.get(italy_data_url).then(res => {
        italy_data = res.data[0]
    }).catch(() => {
        timeout = 1000 * 60 * 2
    })

    setInterval(updateItalyData, timeout)
}

bot.start((ctx) => { 
    ctx.reply("COVID-19 Bot Italia\n\nQuesto 🤖 ti fornirà tutti i dati riguardanti i casi di COVID-19 regione per regione")
    ctx.replyWithMarkdown("Seleziona la regione", { reply_markup: mainMenu })
})

bot.action(/r/, (ctx) => {
    callback_query = ctx.update.callback_query.data
    callback_query = callback_query.substring(1)
    data = regions_data.filter((region) => region.denominazione_regione === callback_query)[0]

    const date = new Date(data.data)
    let formatted_date = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate() + " " + date.getHours() + ":" + (date.getMinutes() < 10 ? '0' : '') + date.getMinutes()


    text = (
        `🇮🇹 *${data.denominazione_regione}* 🇮🇹\n\n`+
        `・ Ricoverati con sintomi: *${data.ricoverati_con_sintomi}*\n` +
        `・ Terapia intensiva: *${data.terapia_intensiva}*\n` +
        `・ Totale ospedalizzati: *${data.totale_ospedalizzati}*\n` +
        `・ Isolamento dom.: *${data.isolamento_domiciliare}*\n` +
        `・ Totale attualmente positivi: *${data.totale_attualmente_positivi}*\n` +
        `・ Nuovi attualmente positivi: *${data.nuovi_attualmente_positivi}*\n` +
        `・ Dimessi guariti: *${data.dimessi_guariti}*\n` +
        `・ Deceduti: *${data.deceduti}*\n` +
        `・ Totale casi: *${data.totale_casi}*\n` +
        `・ Tamponi: *${data.tamponi}*\n` +
        `\nDati aggiornati ${formatted_date}`
    )

    ctx.editMessageText(text, { parse_mode: "Markdown", reply_markup: regionMenu })
});

bot.action(/n/, (ctx) => {
    callback_query = ctx.update.callback_query.data
    callback_query = callback_query.substring(1)

    const date = new Date(italy_data.data)
    let formatted_date = date.getDate()+ "-" + (date.getMonth() + 1) + "-" + date.getFullYear() + " alle " + date.getHours() + ":" + (date.getMinutes() < 10 ? '0' : '') + date.getMinutes()

    text = (
        `🇮🇹 *Italia* 🇮🇹\n\n`+
        `・ Ricoverati con sintomi: *${italy_data.ricoverati_con_sintomi}*\n` +
        `・ Terapia intensiva: *${italy_data.terapia_intensiva}*\n` +
        `・ Totale ospedalizzati: *${italy_data.totale_ospedalizzati}*\n` +
        `・ Isolamento dom.: *${italy_data.isolamento_domiciliare}*\n` +
        `・ Totale attualmente positivi: *${italy_data.totale_attualmente_positivi}*\n` +
        `・ Nuovi attualmente positivi: *${italy_data.nuovi_attualmente_positivi}*\n` +
        `・ Dimessi guariti: *${italy_data.dimessi_guariti}*\n` +
        `・ Deceduti: *${italy_data.deceduti}*\n` +
        `・ Totale casi: *${italy_data.totale_casi}*\n` +
        `・ Tamponi: *${italy_data.tamponi}*\n` +
        `\nDati aggiornati ${formatted_date}`
    )

    ctx.editMessageText(text, { parse_mode: "Markdown", reply_markup: regionMenu })
});

bot.action(/back/, (ctx) => {
    ctx.editMessageText("Seleziona la regione", { reply_markup: mainMenu })
})

updateItalyData()
updateRegionsData()

bot.launch()