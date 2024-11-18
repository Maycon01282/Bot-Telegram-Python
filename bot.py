import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputFile
from telegram.error import BadRequest
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters, Application
from dotenv import load_dotenv
import os
import requests
import qrcode
from io import BytesIO
import emoji

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL")

EMAIL_VALIDATION = range(1)
NEW_CUSTOMER = range(2)
CUSTOMER_REGISTRATION = range(3)
PAYMENT_METHOD = range(4)
ORDER_CONFIRMATION = range(5)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

if not BOT_TOKEN:
    logger.error("Bot token not found. Check the .env file.")
else:
    logger.info(f"Bot token loaded: {BOT_TOKEN}")

if not API_BASE_URL:
    logger.error("API base URL not found. Check the .env file.")
else:
    logger.info(f"API base URL loaded: {API_BASE_URL}")

def fetch_data(endpoint):
    url = f"{API_BASE_URL}/{endpoint}"
    headers = {
        'Authorization': f'Token {BOT_TOKEN}'
    }
    logger.info(f"Fetching data from {url}")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Data fetched: {data}")
        return data
    except requests.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        return None

def generate_keyboard(buttons):
    return InlineKeyboardMarkup([[InlineKeyboardButton(text, callback_data=data)] for text, data in buttons])

def calculate_total_value(cart):
    total = 0
    for prod_id in cart:
        product = fetch_data(f'products/{prod_id}/')
        if product:
            total += product['price']
    return total

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['cart'] = []
    context.user_data['payment_method'] = None

    keyboard = generate_keyboard([("Categories", "categories"), ("Cart", "cart")])
    await update.message.reply_text(
        emoji.emojize(
            'Welcome to our shopping bot! :shopping_cart: Choose an option:\n'
            '1. Click "Categories" to see the products. :package:\n'
            '2. Click "Cart" to see the added items. :shopping_bags:\n'
            '3. After adding products to the cart, complete the purchase by choosing the payment method. :credit_card:'
        ),
        reply_markup=keyboard
    )

async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
            [InlineKeyboardButton("Add more products", callback_data=f"category_{category_id}")],
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
    query = update.callback_query
    await query.answer()
    
    # Log the raw query data
    logging.info(f"Raw query data: {query.data}")
    
    try:
        # Extract the category_id correctly
        data_parts = query.data.split('_')
        logging.info(f"Split query data: {data_parts}")
        
        if len(data_parts) < 2:
            raise ValueError("Invalid query data format.")
        
        category_id = data_parts[1]
        logging.info(f"Fetching products for category {category_id}")
        
        # Construct the URL correctly
        url = f'categories/{category_id}/products/'
        logging.info(f"Fetching data from {url}")
        response = fetch_data(url)
        
        if not response or 'products' not in response:
            raise ValueError(f"Unable to load products for category {category_id}")
        
        products = response['products']
        logging.info(f"Fetched products: {products}")
        
        # Generate the keyboard dynamically
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

    query = update.callback_query
    await query.answer()
    
    data = query.data.split('_')
    logging.info(f"Split query data for add_to_cart: {data}")
    
    if len(data) < 3:
        logging.error(f"Invalid query data format for add_to_cart: {query.data}")
        await query.edit_message_text(text="Invalid product data.")
        return
    
    category_id = data[1]
    product_id = data[2]
    
    if 'cart' not in context.user_data:
        context.user_data['cart'] = []
    context.user_data['cart'].append(product_id)
    logging.info(f"Product {product_id} added to cart")

    # Pergunta ao usuário se deseja adicionar mais produtos ou ir ao carrinho
    keyboard = [
        [InlineKeyboardButton("Add more products", callback_data=f"category_{category_id}")],
        [InlineKeyboardButton("Go to cart", callback_data="cart")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=emoji.emojize("Product added to cart! :white_check_mark: What would you like to do next?"),
        reply_markup=reply_markup
    )

    query = update.callback_query
    await query.answer()
    
    # Log the raw query data
    logging.info(f"Raw query data: {query.data}")
    
    try:
        # Extract the category_id correctly
        data_parts = query.data.split('_')
        logging.info(f"Split query data: {data_parts}")
        
        if len(data_parts) < 2:
            raise ValueError("Invalid query data format.")
        
        category_id = data_parts[1]
        logging.info(f"Fetching products for category {category_id}")
        
        # Construct the URL correctly
        url = f'categories/{category_id}/products/'
        logging.info(f"Fetching data from {url}")
        response = fetch_data(url)
        
        if not response or 'products' not in response:
            raise ValueError(f"Unable to load products for category {category_id}")
        
        products = response['products']
        logging.info(f"Fetched products: {products}")
        
        # Generate the keyboard dynamically
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
    query = update.callback_query
    await query.answer()
    total = calculate_total_value(context.user_data['cart'])
    keyboard = generate_keyboard([("Generate QR Code", "generate_qr"), ("Back to Cart", "cart")])
    await query.edit_message_text(
        text=emoji.emojize(f"Total amount: {total} :moneybag: \nChoose a payment method:"),
        reply_markup=keyboard
    )

async def generate_qr(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    total = calculate_total_value(context.user_data['cart'])
    payment_url = f"{API_BASE_URL}/payment?amount={total}"
    qr_img = qrcode.make(payment_url)
    bio = BytesIO()
    qr_img.save(bio, 'PNG')
    bio.seek(0)
    await query.message.reply_photo(photo=InputFile(bio), caption="Scan this QR code to complete the payment.")

async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    total = calculate_total_value(context.user_data['cart'])
    payment_method = context.user_data['payment_method']
    keyboard = generate_keyboard([("Confirm", "finalize_order"), ("Cancel", "cancel_order")])
    await query.edit_message_text(emoji.emojize(f"Please confirm your order:\n\nTotal: R$ {total:.2f} :moneybag:\nPayment Method: {payment_method}"), reply_markup=keyboard)

async def finalize_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

async def cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(emoji.emojize("Your order has been cancelled. :x:"))

async def existing_customer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=emoji.emojize("Please provide your email for validation: :email:"))
    return EMAIL_VALIDATION

async def email_validation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    email = update.message.text
    await update.message.reply_text(emoji.emojize("Validating your email... :hourglass_flowing_sand:"))
    response = requests.get(f'{API_BASE_URL}/validate_email/?email={email}')
    if response.status_code == 200 and response.json().get('status') == 'success':
        await update.message.reply_text(emoji.emojize("Email successfully validated! :white_check_mark: Please choose the payment method:"))
        return PAYMENT_METHOD
    else:
        await update.message.reply_text(emoji.emojize("Email not found. :x: Please register."))
        return NEW_CUSTOMER

async def new_customer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(emoji.emojize("Please provide your details for registration (Name, Email, Phone): :memo:"))
    return CUSTOMER_REGISTRATION

async def customer_registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    customer_data = update.message.text.split(',')
    data = {
        "name": customer_data[0].strip(),
        "email": customer_data[1].strip(),
        "phone": customer_data[2].strip()
    }
    await update.message.reply_text(emoji.emojize("Registering your details... :hourglass_flowing_sand:"))
    response = requests.post(f'{API_BASE_URL}/clients/create/', json=data)
    if response.status_code == 201:
        await update.message.reply_text(emoji.emojize("Registration successful! :white_check_mark: Please choose the payment method:"))
        return PAYMENT_METHOD
    else:
        await update.message.reply_text(emoji.emojize("Error during registration. :x: Please try again."))
        return NEW_CUSTOMER

async def payment_method(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("Pix", callback_data='pix')],
        [InlineKeyboardButton("Pay on delivery", callback_data='pay_on_delivery')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(emoji.emojize("Choose the payment method: :credit_card:"), reply_markup=reply_markup)

async def pix_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    context.user_data['payment_method'] = 'pix'
    
    total = calculate_total_value(context.user_data['cart'])
    
    pix_data = f"00020126360014BR.GOV.BCB.PIX0114+5511999999995204000053039865404{total:.2f}5802BR5925Receiver Name6009SAO PAULO61080540900062070503***6304"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(pix_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    bio = BytesIO()
    bio.name = 'pix_qrcode.png'
    img.save(bio, 'PNG')
    bio.seek(0)
    
    await query.message.reply_photo(photo=InputFile(bio), caption=emoji.emojize(f"Use the QR Code below to pay R$ {total:.2f} via Pix. :money_with_wings:"))
    await confirm_order(update, context)

async def pay_on_delivery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    context.user_data['payment_method'] = 'pay_on_delivery'
    await confirm_order(update, context)

async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    total = calculate_total_value(context.user_data['cart'])
    payment_method = context.user_data['payment_method']
    keyboard = generate_keyboard([("Confirm", "finalize_order"), ("Cancel", "cancel_order")])
    await query.edit_message_text(emoji.emojize(f"Please confirm your order:\n\nTotal: R$ {total:.2f} :moneybag:\nPayment Method: {payment_method}"), reply_markup=keyboard)

async def finalize_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

async def cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(emoji.emojize("Your order has been cancelled. :x:"))

def setup_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(categories, pattern='^categories$'))
    application.add_handler(CallbackQueryHandler(category, pattern='^category_'))
    application.add_handler(CallbackQueryHandler(product, pattern='^product_'))
    application.add_handler(CallbackQueryHandler(add_to_cart, pattern='^add_to_cart_'))
    application.add_handler(CallbackQueryHandler(cart, pattern='^cart$'))
    application.add_handler(CallbackQueryHandler(checkout, pattern='^checkout$'))
    application.add_handler(CallbackQueryHandler(existing_customer, pattern='^existing_customer$'))
    application.add_handler(CallbackQueryHandler(new_customer, pattern='^new_customer$'))
    application.add_handler(CallbackQueryHandler(payment_method, pattern='^payment_method$'))
    application.add_handler(CallbackQueryHandler(pix_payment, pattern='^pix$'))
    application.add_handler(CallbackQueryHandler(pay_on_delivery, pattern='^pay_on_delivery$'))
    application.add_handler(CallbackQueryHandler(confirm_order, pattern='^confirm_order$'))
    application.add_handler(CallbackQueryHandler(finalize_order, pattern='^finalize_order$'))
    application.add_handler(CallbackQueryHandler(cancel_order, pattern='^cancel_order$'))
    application.add_handler(CallbackQueryHandler(generate_qr, pattern='^generate_qr$'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, email_validation))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, customer_registration))

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    setup_handlers(application)
    application.run_polling()

if __name__ == "__main__":
    main()