import telebot

# Substitua 'YOUR_BOT_TOKEN' pelo token do seu bot
API_TOKEN = 'YOUR_BOT_TOKEN'

bot = telebot.TeleBot(API_TOKEN)

# Comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bem-vindo! Como posso ajudar você?")

# Comando /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Aqui estão os comandos disponíveis:\n/start - Iniciar\n/help - Ajuda")

# Responder a qualquer mensagem de texto
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Iniciar o bot
bot.polling()