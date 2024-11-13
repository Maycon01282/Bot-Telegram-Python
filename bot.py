import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from dotenv import load_dotenv
import os
import requests

# Configuração do logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Corrigido 'levellevel' para 'levelname'
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    logger.error("O token do bot não foi encontrado. Verifique o arquivo .env.")
else:
    logger.info(f"Token do bot carregado: {BOT_TOKEN}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Comando /start recebido")
    keyboard = [
        [InlineKeyboardButton("Categorias de Produtos", callback_data="categorias"),
         InlineKeyboardButton("Clientes", callback_data="clientes")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Escolha uma opção:', reply_markup=reply_markup)

async def list_categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Listando categorias")
    api_url = "http://localhost:8000/categories/list/"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        categories = data.get("categories", [])
        keyboard = [
            [InlineKeyboardButton(category["name"], callback_data=f"categoria_{category['id']}")] 
            for category in categories
        ]
        keyboard.append([InlineKeyboardButton("Voltar", callback_data="voltar")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = update.message or update.callback_query.message
        await message.reply_text("Escolha uma categoria de produto:", reply_markup=reply_markup)
    else:
        message = update.message or update.callback_query.message
        await message.reply_text("Erro ao buscar categorias.")

async def listar_produtos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Listando produtos")
    categoria_id = int(update.callback_query.data.split("_")[1])  # Extrai o ID da categoria
    api_url = f"http://localhost:8000/api/products/list_by_category/?category_id={categoria_id}"
    logger.info(f"URL da API: {api_url}")
    response = requests.get(api_url)
    
    if response.status_code == 200:
        produtos = response.json()
        logger.info(f"Produtos recebidos: {produtos}")
        keyboard = [
            [InlineKeyboardButton(produto["nome"], callback_data=f"produto_{produto['id']}")]
            for produto in produtos
        ]
        keyboard.append([InlineKeyboardButton("Voltar", callback_data="voltar")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.edit_message_text("Escolha um produto:", reply_markup=reply_markup)
    else:
        logger.error(f"Erro ao buscar produtos: {response.status_code} - {response.text}")
        await update.callback_query.edit_message_text("Erro ao buscar produtos.")

async def listar_clientes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Listando clientes")
    response = requests.get("http://localhost:8000/api/clientes/")
    if response.status_code == 200:
        clientes = response.json()
        keyboard = [
            [InlineKeyboardButton(cliente["nome"], callback_data=f"cliente_{cliente['id']}")]
            for cliente in clientes
        ]
        keyboard.append([InlineKeyboardButton("Voltar", callback_data="voltar")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = update.message or update.callback_query.message
        await message.reply_text("Escolha um cliente:", reply_markup=reply_markup)
    else:
        message = update.message or update.callback_query.message
        await message.reply_text("Erro ao buscar clientes.")

async def registrar_pedido(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Registrando pedido")
    cliente_id = int(update.callback_query.data.split("_")[1])  # Extrai o ID do cliente
    produtos_selecionados = context.user_data.get('produtos', [])
    
    if not produtos_selecionados:
        await update.callback_query.edit_message_text("Você não selecionou nenhum produto.")
        return
    
    pedido_data = {
        "cliente_id": cliente_id,
        "produtos": [{"id": produto_id} for produto_id in produtos_selecionados],
    }
    response = requests.post("http://localhost:8000/api/pedidos/", json=pedido_data)
    if response.status_code == 201:
        pedido = response.json()
        context.user_data['pedido_id'] = pedido['id']  # Armazena o ID do pedido
        await update.callback_query.edit_message_text(f"Pedido realizado com sucesso! Seu ID de pedido é {pedido['id']}.")
        context.user_data['produtos'] = []  # Limpa os produtos selecionados
    else:
        await update.callback_query.edit_message_text("Erro ao realizar o pedido.")

async def verificar_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Verificando status do pedido")
    pedido_id = context.user_data.get('pedido_id')
    
    if not pedido_id:
        await update.message.reply_text("Você ainda não fez um pedido.")
        return
    
    response = requests.get(f"http://localhost:8000/api/pedidos/{pedido_id}/status/")
    if response.status_code == 200:
        status = response.json()['status']
        await update.message.reply_text(f"O status do seu pedido é: {status}")
    else:
        await update.message.reply_text("Erro ao verificar o status do pedido.")

async def atualizar_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Atualizando status do pedido")
    pedido_id = context.user_data.get('pedido_id')
    
    if not pedido_id:
        await update.message.reply_text("Você ainda não fez um pedido.")
        return
    
    novo_status = context.args[0] if context.args else "Em preparo"  # Padrão "Em preparo"
    
    # Envia a atualização do status para a API
    response = requests.post(f"http://localhost:8000/api/pedidos/{pedido_id}/status/", json={"status": novo_status})
    
    if response.status_code == 200:
        await update.message.reply_text(f"Status do pedido {pedido_id} atualizado para: {novo_status}")
    else:
        await update.message.reply_text("Erro ao atualizar o status do pedido.")

async def adicionar_produto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Adicionando produto ao pedido")
    produto_id = int(update.callback_query.data.split("_")[1])  # Extrai o ID do produto
    produtos_selecionados = context.user_data.get('produtos', [])
    produtos_selecionados.append(produto_id)
    context.user_data['produtos'] = produtos_selecionados
    await update.callback_query.edit_message_text(f"Produto {produto_id} adicionado ao pedido.")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    logger.info(f"Botão pressionado: {query.data}")
    if query.data == "categorias":
        await list_categories(update, context)
    elif query.data.startswith("categoria_"):
        await listar_produtos(update, context)
    elif query.data == "clientes":
        await listar_clientes(update, context)
    elif query.data.startswith("cliente_"):
        await registrar_pedido(update, context)
    elif query.data.startswith("produto_"):
        await adicionar_produto(update, context)
    elif query.data == "voltar":
        await query.edit_message_text("Voltar ao menu principal.")
        await start(update, context)

def main() -> None:
    logger.info("Iniciando o bot")
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", verificar_status))  # Adicionando comando para verificar status
    application.add_handler(CommandHandler("atualizar_status", atualizar_status))  # Adicionando comando para atualizar status
    application.add_handler(CallbackQueryHandler(button))

    logger.info("Bot iniciado")
    application.run_polling()

if __name__ == "__main__":
    main()