import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
from dotenv import load_dotenv
import os
import requests
import qrcode
from io import BytesIO
import emoji

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

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    logger.error("Bot token not found. Check the .env file.")
else:
    logger.info(f"Bot token loaded: {BOT_TOKEN}")

# Function to calculate the total value of the cart
def calculate_total_value(cart):
    total = 0
    for prod_id in cart:
        response = requests.get(f'http://localhost:8000/products/{prod_id}/')
        product = response.json()
        total += product['price']
    return total

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['cart'] = []
    context.user_data['payment_method'] = None
    
    keyboard = [
        [InlineKeyboardButton("Categories", callback_data='categories')],
        [InlineKeyboardButton("Cart", callback_data='cart')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        emoji.emojize(
            'Welcome to our shopping bot! :shopping_cart: Choose an option:\n'
            '1. Click "Categories" to see the products. :package:\n'
            '2. Click "Cart" to see the added items. :shopping_bags:\n'
            '3. After adding products to the cart, complete the purchase by choosing the payment method. :credit_card:',
            use_aliases=True
        ),
        reply_markup=reply_markup
    )

async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    # Fetch categories from API
    response = requests.get('http://localhost:8000/categories/list/')
    categories = response.json()
    
    keyboard = [[InlineKeyboardButton(cat['name'], callback_data=f"category_{cat['id']}")] for cat in categories]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=emoji.emojize("Choose a category: :package:", use_aliases=True), reply_markup=reply_markup)

async def category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    category_id = query.data.split('_')[1]
    
    # Fetch products from API
    response = requests.get(f'http://localhost:8000/categories/{category_id}/products/')
    products = response.json()
    
    keyboard = [[InlineKeyboardButton(prod['name'], callback_data=f"product_{prod['id']}")] for prod in products]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=emoji.emojize("Choose a product: :shopping_bags:", use_aliases=True), reply_markup=reply_markup)

async def product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    product_id = query.data.split('_')[1]
    
    # Fetch product details from API
    response = requests.get(f'http://localhost:8000/products/{product_id}/')
    product = response.json()
    
    keyboard = [
        [InlineKeyboardButton("Add to cart", callback_data=f"add_to_cart_{product_id}")],
        [InlineKeyboardButton("Back", callback_data='categories')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=emoji.emojize(
            f"Product details:\n\n{product['name']}\n{product['description']}\nPrice: {product['price']} :moneybag:",
            use_aliases=True
        ),
        reply_markup=reply_markup
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
    
    # Fetch product details for items in cart
    products = [requests.get(f'http://localhost:8000/products/{prod_id}/').json() for prod_id in cart]
    
    cart_text = "\n".join([f"{prod['name']} - {prod['price']}" for prod in products])
    keyboard = [[InlineKeyboardButton("Checkout", callback_data='checkout')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=emoji.emojize(f"Your cart:\n\n{cart_text} :shopping_cart:", use_aliases=True), reply_markup=reply_markup)

async def checkout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data='existing_customer')],
        [InlineKeyboardButton("No", callback_data='new_customer')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=emoji.emojize("Are you already our customer? :bust_in_silhouette:", use_aliases=True), reply_markup=reply_markup)

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
    response = requests.get(f'http://localhost:8000/clients/?email={email}')
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
    response = requests.post('http://localhost:8000/clients/create/', json=data)
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
    keyboard = [
        [InlineKeyboardButton("Confirm", callback_data='finalize_order')],
        [InlineKeyboardButton("Cancel", callback_data='cancel_order')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(emoji.emojize(f"Please confirm your order:\n\nTotal: R$ {total:.2f} :moneybag:\nPayment Method: {payment_method}", use_aliases=True), reply_markup=reply_markup)

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
    response = requests.post('http://localhost:8000/orders/create/', json=data)
    if response.status_code == 201:
        await query.edit_message_text(emoji.emojize("Your order has been confirmed! :white_check_mark: Track the status of your order through our system.", use_aliases=True))
        context.user_data['cart'].clear()  # Clear the cart after order confirmation
    else:
        await query.edit_message_text(emoji.emojize(f"Error confirming order: {response.json().get('detail', 'Unknown error')} :x:. Please try again.", use_aliases=True))

async def cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(emoji.emojize("Your order has been cancelled. :x:", use_aliases=True))

def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(existing_customer, pattern='^existing_customer$'))
    application.add_handler(CallbackQueryHandler(new_customer, pattern='^new_customer$'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, email_validation))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, customer_registration))
    application.add_handler(CallbackQueryHandler(payment_method, pattern='^payment_method$'))
    application.add_handler(CallbackQueryHandler(pix_payment, pattern='^pix$'))
    application.add_handler(CallbackQueryHandler(pay_on_delivery, pattern='^pay_on_delivery$'))
    application.add_handler(CallbackQueryHandler(confirm_order, pattern='^confirm_order$'))
    application.add_handler(CallbackQueryHandler(finalize_order, pattern='^finalize_order$'))
    application.add_handler(CallbackQueryHandler(cancel_order, pattern='^cancel_order$'))
    
    application.run_polling()

if __name__ == '__main__':
    main()