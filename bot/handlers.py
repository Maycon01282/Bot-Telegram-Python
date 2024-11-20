import logging
import os
import emoji
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputFile
from telegram.ext import CallbackQueryHandler, MessageHandler, filters, ContextTypes, CommandHandler, ConversationHandler
from bot.pixqrcodegen import Payload
from bot.utils import *
from bot.states import EMAIL_VALIDATION, NEW_CUSTOMER, CUSTOMER_REGISTRATION, PAYMENT_METHOD, ORDER_CONFIRMATION

logger = logging.getLogger(__name__)

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    context.user_data['cart'] = []
    context.user_data['payment_method'] = None

    keyboard = generate_keyboard([
        ("Categories", "categories"),
        ("Cart", "cart"),
        ("Talk to Agent", "talk_to_agent")
    ])
    await update.message.reply_text(
        emoji.emojize(
            'Welcome to our shopping bot! :shopping_cart: Choose an option:\n'
            '1. Click "Categories" to see the products. :package:\n'
            '2. Click "Cart" to see the added items. :shopping_bags:\n'
            '3. After adding products to the cart, complete the purchase by choosing the payment method. :credit_card:\n'
            '4. Click "Talk to Agent" to speak with a representative. :telephone_receiver:'
        ),
        reply_markup=keyboard
    )

async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the categories callback query."""
    query = update.callback_query
    await query.answer()

    logger.info("Fetching categories")
    response = fetch_data('categories/list/')
    if not response or 'categories' not in response:
        logger.error("Unable to load categories")
        await query.edit_message_text(text="Unable to load categories.")
        return

    categories = response['categories']
    logger.info(f"Fetched categories: {categories}")
    keyboard = generate_keyboard([(cat['name'], f"category_{cat['id']}") for cat in categories])
    await query.edit_message_text(text=emoji.emojize("Choose a category: :package:"), reply_markup=keyboard)

async def add_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Log the raw query data
    logging.info(f"Raw query data for add_to_cart: {query.data}")

    try:
        # Extract the category_id and product_id correctly
        data_parts = query.data.split('_')
        logging.info(f"Split query data for add_to_cart: {data_parts}")

        if len(data_parts) < 4:
            logging.error(f"Invalid query data format for add_to_cart: {query.data}")
            await query.edit_message_text(text="Invalid product data.")
            return

        category_id = data_parts[2]
        product_id = data_parts[3]

        # Add product to cart
        if 'cart' not in context.user_data:
            context.user_data['cart'] = []
        context.user_data['cart'].append(product_id)
        logging.info(f"Product {product_id} added to cart")

        # Pergunta ao usuário se deseja adicionar mais produtos ou ir ao carrinho
        keyboard = [
            [InlineKeyboardButton("Add more products", callback_data="categories")],
            [InlineKeyboardButton("Go to cart", callback_data="cart")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=emoji.emojize("Product added to cart! :white_check_mark: What would you like to do next?"),
            reply_markup=reply_markup
        )

    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
        await query.edit_message_text(text=str(ve))

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        await query.edit_message_text(text="An unexpected error occurred. Please try again.")

async def category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the category callback query."""
    query = update.callback_query
    await query.answer()
    
    logging.info(f"Raw query data: {query.data}")
    
    try:
        data_parts = query.data.split('_')
        logging.info(f"Split query data: {data_parts}")
        
        if len(data_parts) < 2:
            raise ValueError("Invalid query data format.")
        
        category_id = data_parts[1]
        logging.info(f"Fetching products for category {category_id}")
        
        url = f'categories/{category_id}/products/'
        logging.info(f"Fetching data from {url}")
        response = fetch_data(url)
        
        if not response or 'products' not in response:
            raise ValueError(f"Unable to load products for category {category_id}")
        
        products = response['products']
        logging.info(f"Fetched products: {products}")
        
        keyboard = generate_keyboard([
            (prod['name'], f"product_{prod['id']}") for prod in products
        ])
        
        await query.edit_message_text(
            text=emoji.emojize("Choose a product: :shopping_bags:"),
            reply_markup=keyboard
        )

    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
        await query.edit_message_text(text=str(ve))

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        await query.edit_message_text(text="An unexpected error occurred. Please try again.")

async def product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the product callback query."""
    query = update.callback_query
    await query.answer()
    product_id = query.data.split('_')[1]
    product = fetch_data(f'products/{product_id}/')
    if not product:
        await query.edit_message_text(text="Unable to load product details.")
        return

    photo_path = f"./media/product_photos/{product['photo'].split('/')[-1]}"
    logging.info(f"Photo Path: {photo_path}")

    if not os.path.exists(photo_path):
        logging.error(f"Photo file does not exist: {photo_path}")
        await query.edit_message_text(text="Unable to load product photo.")
        return
    
    keyboard = generate_keyboard([("Add to cart", f"add_to_cart_{product_id}"), ("Back", 'categories')])
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(photo_path, 'rb'),
        caption=emoji.emojize(
            f"Product details:\n\n{product['name']}\n{product['description']}\nPrice: {product['price']} :moneybag:"
        ),
        reply_markup=keyboard
    )

async def cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    cart = context.user_data.get('cart', [])
    if not cart:
        await query.edit_message_text(text=emoji.emojize("Your cart is empty. :shopping_cart:"))
        return
    products = [fetch_data(f'products/{prod_id}/') for prod_id in cart]
    products = [prod for prod in products if prod]
    cart_text = "\n".join([f"{prod['name']} - {prod['price']}" for prod in products])
    keyboard = generate_keyboard([("Checkout", 'checkout')])
    await query.edit_message_text(text=emoji.emojize(f"Your cart:\n\n{cart_text} :shopping_cart:"), reply_markup=keyboard)

async def checkout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the checkout callback query."""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("Existing Customer", callback_data='existing_customer')],
        [InlineKeyboardButton("New Customer", callback_data='new_customer')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=emoji.emojize("Are you an existing customer or a new customer?"),
        reply_markup=reply_markup
    )

async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the confirm order callback query."""
    query = update.callback_query
    await query.answer()
    total = calculate_total_value(context.user_data['cart'])
    payment_method = context.user_data['payment_method']
    keyboard = generate_keyboard([("Confirm", "finalize_order"), ("Cancel", "cancel_order")])
    await query.edit_message_text(emoji.emojize(f"Please confirm your order:\n\nTotal: R$ {total:.2f} :moneybag:\nPayment Method: {payment_method}"), reply_markup=keyboard)

async def finalize_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the finalize order callback query."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(emoji.emojize("Creating your order... :hourglass_flowing_sand:"))
    total = calculate_total_value(context.user_data['cart'])
    data = {
        "payment_method": context.user_data['payment_method'],
        "products": context.user_data['cart'],
        "amount": total
    }
    response = requests.post(f'{API_BASE_URL}/orders/create/', json=data)
    if response.status_code == 201:
        await query.edit_message_text(emoji.emojize("Your order has been confirmed! :white_check_mark: Track the status of your order through our system."))
        context.user_data['cart'].clear()
    else:
        await query.edit_message_text(emoji.emojize(f"Error confirming order: {response.json().get('detail', 'Unknown error')} :x:. Please try again."))

async def existing_customer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the existing customer callback query."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=emoji.emojize("Please provide your email for validation: :email:"))
    return EMAIL_VALIDATION

async def email_validation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the email validation message."""
    email = update.message.text
    logging.info(f"Validating email: {email}")
    await update.message.reply_text(emoji.emojize("Validating your email... :hourglass_flowing_sand:"))
    try:
        response = requests.get(f'{API_BASE_URL}/clients/validate_email/?email={email}')
        logging.info(f"API response status code: {response.status_code}")
        logging.info(f"API response content: {response.content}")
        if response.status_code == 200 and response.json().get('status') == 'success':
            logging.info("Email validation successful, transitioning to PAYMENT_METHOD state.")
            await update.message.reply_text(emoji.emojize("Email successfully validated! :white_check_mark: Please choose the payment method:"))
            return PAYMENT_METHOD
        else:
            logging.info("Email validation failed, transitioning to CUSTOMER_REGISTRATION state.")
            await update.message.reply_text(emoji.emojize("Email not found. :x: Please provide your details for registration (Name, Email, Phone, City, Address): :memo:"))
            return CUSTOMER_REGISTRATION
    except Exception as e:
        logging.error(f"Exception during email validation: {e}")
        await update.message.reply_text(emoji.emojize("An error occurred during email validation. :x: Please try again later."))
        return CUSTOMER_REGISTRATION

async def new_customer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the new customer callback query."""
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(emoji.emojize("Please provide your details for registration (Name, Email, Phone, City, Address): :memo:"))
    return CUSTOMER_REGISTRATION

async def customer_registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the customer registration message."""
    logging.info("Starting customer registration process.")
    customer_data = update.message.text.split(',')
    if len(customer_data) != 5:
        await update.message.reply_text(emoji.emojize("Invalid input format. Please provide your details in the format: Name, Email, Phone, City, Address"))
        return CUSTOMER_REGISTRATION

    data = {
        "name": customer_data[0].strip(),
        "email": customer_data[1].strip(),
        "phone_number": customer_data[2].strip(),  # Corrigido para 'phone_number'
        "city": customer_data[3].strip(),
        "address": customer_data[4].strip()
    }
    logging.info(f"Customer data: {data}")

    await update.message.reply_text(emoji.emojize("Registering your details... :hourglass_flowing_sand:"))
    try:
        response = requests.post(f'{API_BASE_URL}/clients/create/', json=data)
        logging.info(f"API response status code: {response.status_code}")
        logging.info(f"API response content: {response.content}")
        if response.status_code == 201:
            await update.message.reply_text(emoji.emojize("Registration successful! :white_check_mark: Please choose the payment method:"))
            return PAYMENT_METHOD
        else:
            await update.message.reply_text(emoji.emojize("Registration failed. :x: Please try again."))
            return CUSTOMER_REGISTRATION
    except Exception as e:
        logging.error(f"Exception during registration: {e}")
        await update.message.reply_text(emoji.emojize("An error occurred during registration. :x: Please try again later."))
        return CUSTOMER_REGISTRATION

async def payment_method(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the payment method callback query."""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("Pix", callback_data='pix_payment')],
        [InlineKeyboardButton("Pay on delivery", callback_data='pay_on_delivery')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    logging.info("Displaying payment method options.")
    
    try:
        await query.edit_message_text(emoji.emojize("Choose the payment method: :credit_card:"), reply_markup=reply_markup)
        logging.info("Payment method options displayed successfully.")
    except Exception as e:
        logging.error(f"Error displaying payment method options: {e}")
    
    return PAYMENT_METHOD

async def pix_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the Pix payment callback query."""
    query = update.callback_query
    await query.answer()
    
    context.user_data['payment_method'] = 'pix'
    
    total = calculate_total_value(context.user_data['cart'])
    
    pix_key = os.getenv("PIX_KEY")
    receiver_name = os.getenv("RECEIVER_NAME")
    city = os.getenv("RECEIVER_CITY")
    txid = os.getenv("TXID", "123456789")
    
    # Gerar o payload e o QR Code usando a classe Payload
    payload = Payload(receiver_name, pix_key, f"{total:.2f}", city, txid)
    payload.gerarPayload()
    
    # Carregar a imagem do QR Code gerado
    qr_code_path = os.path.expanduser(os.path.join(payload.diretorioQrCode, 'pixqrcodegen.png'))
    with open(qr_code_path, 'rb') as qr_code_file:
        await query.message.reply_photo(photo=InputFile(qr_code_file), caption=emoji.emojize(f"Use the QR Code below to pay R$ {total:.2f} via Pix. :money_with_wings:"))
    
    await confirm_order(update, context)

async def pay_on_delivery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the pay on delivery callback query."""
    query = update.callback_query
    await query.answer()
    
    context.user_data['payment_method'] = 'pay_on_delivery'
    await confirm_order(update, context)

async def cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the cancel order callback query."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(emoji.emojize("Your order has been cancelled. :x:"))
    
async def talk_to_agent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the talk to agent callback query."""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        text=emoji.emojize("An agent will contact you soon. :telephone_receiver:")
    )
    
    agent_chat_id = os.getenv("AGENT_CHAT_ID")
    if agent_chat_id:
        await context.bot.send_message(
            chat_id=agent_chat_id,
            text=f"User {update.effective_user.username} ({update.effective_user.id}) requested to talk to an agent."
        )
    else:
        logging.error("AGENT_CHAT_ID not configured in .env")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the cancel command."""
    await update.message.reply_text(emoji.emojize("Operation cancelled. :x:"))
    return ConversationHandler.END

def setup_handlers(application):
    """Setup all handlers for the application."""
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            EMAIL_VALIDATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, email_validation)],
            CUSTOMER_REGISTRATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, customer_registration)],
            PAYMENT_METHOD: [CallbackQueryHandler(pix_payment, pattern='^pix_payment$'),
                             CallbackQueryHandler(pay_on_delivery, pattern='^pay_on_delivery$')],
            # outros estados
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_message=True  # Adicione esta linha para garantir que os handlers sejam rastreados para cada mensagem
    )

    application.add_handler(conv_handler)
    add_callback_handlers(application)
    add_message_handlers(application)

def add_callback_handlers(application):
    """Add all callback query handlers."""
    application.add_handler(CallbackQueryHandler(new_customer, pattern='^new_customer$'))
    application.add_handler(CallbackQueryHandler(payment_method, pattern='^payment_method$'))
    application.add_handler(CallbackQueryHandler(pix_payment, pattern='^pix_payment$'))
    application.add_handler(CallbackQueryHandler(pay_on_delivery, pattern='^pay_on_delivery$'))
    application.add_handler(CallbackQueryHandler(confirm_order, pattern='^confirm_order$'))
    application.add_handler(CallbackQueryHandler(finalize_order, pattern='^finalize_order$'))
    application.add_handler(CallbackQueryHandler(cancel_order, pattern='^cancel_order$'))
    application.add_handler(CallbackQueryHandler(talk_to_agent, pattern='^talk_to_agent$'))
    application.add_handler(CallbackQueryHandler(categories, pattern='^categories$'))
    application.add_handler(CallbackQueryHandler(add_to_cart, pattern='^add_to_cart_'))
    application.add_handler(CallbackQueryHandler(category, pattern='^category_'))
    application.add_handler(CallbackQueryHandler(product, pattern='^product_'))
    application.add_handler(CallbackQueryHandler(cart, pattern='^cart$'))
    application.add_handler(CallbackQueryHandler(checkout, pattern='^checkout$'))
    application.add_handler(CallbackQueryHandler(existing_customer, pattern='^existing_customer$'))
    application.add_handler(CallbackQueryHandler(categories, pattern='^categories_\\d+$'))

def add_message_handlers(application):
    """Add all message handlers."""
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex(r'^[^,]+,[^,]+,[^,]+,[^,]+,[^,]+$'), customer_registration))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, email_validation))
    application.add_handler(MessageHandler(filters.COMMAND, start))