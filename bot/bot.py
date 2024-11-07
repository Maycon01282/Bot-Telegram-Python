import requests
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import os

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = requests.get("http://localhost:8000/api/user/")
    print(response.json())
    for user in response.json():
        await update.message.reply_text(f'{user["name"]} | {user["email"]}')

async def Pedido(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Pedido do {update.effective_user.first_name} foi uma coca')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Usuários", callback_data="Usuarios"),
            InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [InlineKeyboardButton("Option 3", callback_data="3")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please choose:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == "Usuarios":
        response = requests.get("http://localhost:8000/api/user/")
        keyboard = []
        
        for user in response.json():
            keyboard.append([InlineKeyboardButton(user["name"], callback_data=user["name"])])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Escolha um usuário:", reply_markup=reply_markup)
        return
    
    await query.edit_message_text(text=f"Selected option: {query.data}")

# Use uma variável de ambiente para a chave do bot por segurança
BOT_TOKEN = os.getenv("BOT_TOKEN", "7202444496:AAG8ZSQw1S-nXsbHsnxX4h_lGB3XaJ6QzuI")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("teste", hello))
app.add_handler(CommandHandler("pedido", Pedido))
app.add_handler(CommandHandler("key", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()