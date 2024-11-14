import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters, Application
from dotenv import load_dotenv
import os
import requests
import qrcode
from io import BytesIO
import emoji

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL")

# Bot states definition
EMAIL_VALIDATION = range(1)
NEW_CUSTOMER = range(2)
CUSTOMER_REGISTRATION = range(3)
PAYMENT_METHOD = range(4)
ORDER_CONFIRMATION = range(5)

# Logging configuration
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

# Function to centralize HTTP requests with error handling
def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch data from {endpoint}: {e}")
        return None

# Function to build dynamic option keyboards
def generate_keyboard(buttons):
    return InlineKeyboardMarkup([[InlineKeyboardButton(text, callback_data=data)] for text, data in buttons])

# Function to calculate the total value of the cart
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
            '3. After adding products to the cart, complete the purchase by choosing the payment method. :credit_card:',
            use_aliases=True
        ),
        reply_markup=keyboard
    )

async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    # Fetch categories from API
    categories = fetch_data('categories/list/')
    if not categories:
        await query.edit_message_text(text="Unable to load categories.")
        return

    keyboard = generate_keyboard([(cat['name'], f"category_{cat['id']}") for cat in categories])
    await query.edit_message_text(text=emoji.emojize("Choose a category: :package:", use_aliases=True), reply_markup=keyboard)

async def category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    category_id = query.data.split('_')[1]
    products = fetch_data(f'categories/{category_id}/products/')
    if not products:
        await query.edit_message_text(text="Unable to load products.")
        return

    keyboard = generate_keyboard([(prod['name'], f"product_{prod['id']}") for prod in products])
    await query.edit_message_text(text=emoji.emojize("Choose a product: :shopping_bags:", use_aliases=True), reply_markup=keyboard)

async def product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    product_id = query.data.split('_')[1]
    product = fetch_data(f'products/{product_id}/')
    if not product:
        await query.edit_message_text(text="Unable to load product details.")
        return

    keyboard = generate_keyboard([("Add to cart", f"add_to_cart_{product_id}"), ("Back", 'categories')])
    await query.edit_message_text(
        text=emoji.emojize(
            f"Product details:\n\n{product['name']}\n{product['description']}\nPrice: {product['price']} :moneybag:",
            use_aliases=True
        ),
        reply_markup=keyboard
    )

async def add_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    product_id = query.data.split('_')[2]
    context.user_data['cart'].append(product_id)
    
    await query.edit_message_text(text=emoji.emojize("Product added to cart! :white_check_mark:", use_aliases=True))

async def cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    cart = context.user_data.get('cart', [])
    if not cart:
        await query.edit_message_text(text=emoji.emojize("Your cart is empty. :shopping_cart:", use_aliases=True))
        return

    products = [fetch_data(f'products/{prod_id}/') for prod_id in cart]
    products = [prod for prod in products if prod]
    
    cart_text = "\n".join([f"{prod['name']} - {prod['price']}" for prod in products])
    keyboard = generate_keyboard([("Checkout", 'checkout')])
    await query.edit_message_text(text=emoji.emojize(f"Your cart:\n\n{cart_text} :shopping_cart:", use_aliases=True), reply_markup=keyboard)

async def checkout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    total = calculate_total_value(context.user_data['cart'])
    keyboard = generate_keyboard([("Generate QR Code", "generate_qr"), ("Back to Cart", "cart")])
    await query.edit_message_text(
        text=emoji.emojize(f"Total amount: {total} :moneybag: \nChoose a payment method:", use_aliases=True),
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
    
    # Confirm order details before sending to API
    total = calculate_total_value(context.user_data['cart'])
    payment_method = context.user_data['payment_method']
    keyboard = generate_keyboard([("Confirm", "finalize_order"), ("Cancel", "cancel_order")])
    await query.edit_message_text(emoji.emojize(f"Please confirm your order:\n\nTotal: R$ {total:.2f} :moneybag:\nPayment Method: {payment_method}", use_aliases=True), reply_markup=keyboard)

async def finalize_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    # Provide feedback while creating order
    await query.edit_message_text(emoji.emojize("Creating your order... :hourglass_flowing_sand:", use_aliases=True))
    
    # Create order with API
    total = calculate_total_value(context.user_data['cart'])
    data = {
        "payment_method": context.user_data['payment_method'],
        "products": context.user_data['cart'],
        "amount": total
    }
    response = requests.post(f'{API_BASE_URL}/orders/create/', json=data)
    if response.status_code == 201:
        await query.edit_message_text(emoji.emojize("Your order has been confirmed! :white_check_mark: Track the status of your order through our system.", use_aliases=True))
        context.user_data['cart'].clear()  # Clear the cart after order confirmation
    else:
        await query.edit_message_text(emoji.emojize(f"Error confirming order: {response.json().get('detail', 'Unknown error')} :x:. Please try again.", use_aliases=True))

async def cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(emoji.emojize("Your order has been cancelled. :x:", use_aliases=True))

async def existing_customer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(text=emoji.emojize("Please provide your email for validation: :email:", use_aliases=True))

    return EMAIL_VALIDATION

async def email_validation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    email = update.message.text
    
    # Provide feedback while validating email
    await update.message.reply_text(emoji.emojize("Validating your email... :hourglass_flowing_sand:", use_aliases=True))
    
    # Validate email with API
    response = requests.get(f'{API_BASE_URL}/clients/?email={email}')
    if response.status_code == 200 and response.json():
        await update.message.reply_text(emoji.emojize("Email successfully validated! :white_check_mark: Please choose the payment method:", use_aliases=True))
        return PAYMENT_METHOD
    else:
        await update.message.reply_text(emoji.emojize("Email not found. :x: Please register.", use_aliases=True))
        return NEW_CUSTOMER

async def new_customer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(emoji.emojize("Please provide your details for registration (Name, Email, Phone): :memo:", use_aliases=True))
    return CUSTOMER_REGISTRATION

async def customer_registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    customer_data = update.message.text.split(',')
    data = {
        "name": customer_data[0].strip(),
        "email": customer_data[1].strip(),
        "phone": customer_data[2].strip()
    }
    
    # Provide feedback while registering
    await update.message.reply_text(emoji.emojize("Registering your details... :hourglass_flowing_sand:", use_aliases=True))
    
    # Register new customer with API
    response = requests.post(f'{API_BASE_URL}/clients/create/', json=data)
    if response.status_code == 201:
        await update.message.reply_text(emoji.emojize("Registration successful! :white_check_mark: Please choose the payment method:", use_aliases=True))
        return PAYMENT_METHOD
    else:
        await update.message.reply_text(emoji.emojize("Error during registration. :x: Please try again.", use_aliases=True))
        return NEW_CUSTOMER

async def payment_method(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("Pix", callback_data='pix')],
        [InlineKeyboardButton("Pay on delivery", callback_data='pay_on_delivery')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(emoji.emojize("Choose the payment method: :credit_card:", use_aliases=True), reply_markup=reply_markup)

async def pix_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    context.user_data['payment_method'] = 'pix'
    
    # Calculate the total value of the cart
    total = calculate_total_value(context.user_data['cart'])
    
    # Generate the QR Code for Pix payment
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
    
    await query.message.reply_photo(photo=InputFile(bio), caption=emoji.emojize(f"Use the QR Code below to pay R$ {total:.2f} via Pix. :money_with_wings:", use_aliases=True))
    await confirm_order(update, context)

async def pay_on_delivery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    context.user_data['payment_method'] = 'pay_on_delivery'
    await confirm_order(update, context)

async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    # Confirm order details before sending to API
    total = calculate_total_value(context.user_data['cart'])
    payment_method = context.user_data['payment_method']
    keyboard = generate_keyboard([("Confirm", "finalize_order"), ("Cancel", "cancel_order")])
    await query.edit_message_text(emoji.emojize(f"Please confirm your order:\n\nTotal: R$ {total:.2f} :moneybag:\nPayment Method: {payment_method}", use_aliases=True), reply_markup=keyboard)

async def finalize_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    # Provide feedback while creating order
    await query.edit_message_text(emoji.emojize("Creating your order... :hourglass_flowing_sand:", use_aliases=True))
    
    # Create order with API
    total = calculate_total_value(context.user_data['cart'])
    data = {
        "payment_method": context.user_data['payment_method'],
        "products": context.user_data['cart'],
        "amount": total
    }
    response = requests.post(f'{API_BASE_URL}/orders/create/', json=data)
    if response.status_code == 201:
        await query.edit_message_text(emoji.emojize("Your order has been confirmed! :white_check_mark: Track the status of your order through our system.", use_aliases=True))
        context.user_data['cart'].clear()  # Clear the cart after order confirmation
    else:
        await query.edit_message_text(emoji.emojize(f"Error confirming order: {response.json().get('detail', 'Unknown error')} :x:. Please try again.", use_aliases=True))

async def cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(emoji.emojize("Your order has been cancelled. :x:", use_aliases=True))

def setup_handlers(application):
    # Handlers for callback queries
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

    # Handlers for text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, email_validation))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, customer_registration))

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    setup_handlers(application)
    application.run_polling()

if __name__ == '__main__':
    main()
