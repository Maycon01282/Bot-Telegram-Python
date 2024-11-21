import logging
import os
import requests
import aiohttp
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputFile
from telegram.ext import CallbackQueryHandler, MessageHandler, filters, ContextTypes, CommandHandler, ConversationHandler
from bot.pixqrcodegen import Payload
from bot.utils import *
from bot.states import EMAIL_VALIDATION, NEW_CUSTOMER, CUSTOMER_REGISTRATION, PAYMENT_METHOD, ORDER_CONFIRMATION, PAYMENT_METHOD_CHOICE

logger = logging.getLogger(__name__)

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start the bot and initialize user data."""
    context.user_data['cart'] = []
    context.user_data['payment_method'] = None

    keyboard = generate_keyboard([
        ("Categories", "categories"),
        ("Cart", "cart"),
        ("Talk to Agent", "talk_to_agent")
    ])
    await update.message.reply_text(
        'Welcome to our shopping bot! Choose an option:\n'
        '1. Click "Categories" to see the products.\n'
        '2. Click "Cart" to see the added items.\n'
        '3. After adding products to the cart, complete the purchase by choosing the payment method.\n'
        '4. Click "Talk to Agent" to speak with a representative.',
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
    keyboard.append([InlineKeyboardButton("Back to Start", callback_data="start")])
    await query.edit_message_text(text="Choose a category:", reply_markup=InlineKeyboardMarkup(keyboard))

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
        product_id = int(data_parts[3])

        # Add product to cart
        if 'cart' not in context.user_data:
            context.user_data['cart'] = []

        # Check if the product is already in the cart
        for item in context.user_data['cart']:
            if item['product_id'] == product_id:
                item['quantity'] += 1
                break
        else:
            context.user_data['cart'].append({"product_id": product_id, "quantity": 1})

        logging.info(f"Product {product_id} added to cart")

        # Ask the user if they want to add more products or go to the cart
        keyboard = [
            [InlineKeyboardButton("Add more products", callback_data="categories")],
            [InlineKeyboardButton("Go to cart", callback_data="cart")],
            [InlineKeyboardButton("Back to Start", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Product added to cart! What would you like to do next?",
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
        keyboard.append([InlineKeyboardButton("Back to Start", callback_data="start")])
        
        await query.edit_message_text(
            text="Choose a product:",
            reply_markup=InlineKeyboardMarkup(keyboard)
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
    keyboard.append([InlineKeyboardButton("Back to Start", callback_data="start")])
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(photo_path, 'rb'),
        caption=(
            f"Product details:\n\n{product['name']}\n{product['description']}\nPrice: {product['price']}"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    cart = context.user_data.get('cart', [])
    if not cart:
        await query.edit_message_text(text="Your cart is empty.")
        return

    # Fetch product details for each item in the cart
    products = []
    async with aiohttp.ClientSession() as session:
        for item in cart:
            product_id = item['product_id']
            quantity = item['quantity']
            async with session.get(f'{API_BASE_URL}/products/{product_id}/', params={'quantity': quantity}) as response:
                if response.status == 200:
                    products.append(await response.json())
                else:
                    logging.error(f"Error fetching product data: {response.status} - {await response.text()}")

    # Generate cart text
    cart_text = "\n".join([f"{prod['name']} - {prod['price']} (Quantity: {item['quantity']})" for prod, item in zip(products, cart)])
    keyboard = generate_keyboard([("Checkout", 'checkout')])
    keyboard.append([InlineKeyboardButton("Back to Start", callback_data="start")])
    await query.edit_message_text(text=f"Your cart:\n\n{cart_text}", reply_markup=InlineKeyboardMarkup(keyboard))

async def checkout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the checkout callback query."""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("Existing Customer", callback_data='existing_customer')],
        [InlineKeyboardButton("New Customer", callback_data='new_customer')],
        [InlineKeyboardButton("Back to Start", callback_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Are you an existing customer or a new customer?",
        reply_markup=reply_markup
    )

async def order_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the order confirmation."""
    if update.message.photo:
        # The customer sent a photo (payment receipt)
        file_id = update.message.photo[-1].file_id
        new_file = await context.bot.get_file(file_id)
        await new_file.download(f'comprovantes/{file_id}.jpg')
        logging.info(f"Payment receipt received and saved as comprovantes/{file_id}.jpg")

        await update.message.reply_text("Payment receipt received. Your order is being processed.")
        # Here you can add the logic to finalize the order
        return ConversationHandler.END
    else:
        await update.message.reply_text("Please send the payment receipt as a photo.")
        return ORDER_CONFIRMATION

async def finalize_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the finalize order callback query."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Creating your order...")

    total = calculate_total_value(context.user_data['cart'])
    order_data = {
        "client": context.user_data['client_id'],  # Assuming you have client_id stored in user_data
        "payment_method": context.user_data['payment_method'],
        "amount": total,
        "status": "new"  # Default status
    }

    logging.info(f"Order data: {order_data}")

    # Create the order
    order_id = await create_order(order_data)
    if not order_id:
        await query.edit_message_text("Error confirming order: Unable to create order. Please try again.")
        return

    logging.info(f"Order ID: {order_id}")
    logging.info(f"Cart content: {context.user_data['cart']}")

    # Create order items
    for item in context.user_data['cart']:
        logging.info(f"Processing cart item: {item}")
        product_id = item['product_id']
        quantity = item['quantity']
        order_item_data = {
            "order": order_id,
            "product": product_id,
            "quantity": quantity
        }
        await create_order_item(order_item_data)

    await query.edit_message_text("Your order has been confirmed! Track the status of your order through our system.")
    context.user_data['cart'].clear()

async def create_order(order_data):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{API_BASE_URL}/orders/create/', json=order_data) as response:
            logging.info(f"Order creation response status code: {response.status}")
            response_content = await response.text()
            logging.info(f"Order creation response content: {response_content}")
            if response.status == 201:
                return (await response.json()).get('id')
            else:
                logging.error(f"Error creating order: {response.status} - {response_content}")
                return None

async def create_order_item(order_item_data):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{API_BASE_URL}/order_items/create/', json=order_item_data) as response:
            logging.info(f"Order item creation response status code: {response.status}")
            response_content = await response.text()
            logging.info(f"Order item creation response content: {response_content}")
            if response.status == 201:
                return True
            else:
                logging.error(f"Error creating order item: {response.status} - {response_content}")
                return False

async def existing_customer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the existing customer callback query."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Please provide your email for validation:")
    return EMAIL_VALIDATION

async def email_validation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the email validation message."""
    email = update.message.text
    logging.info(f"Validating email: {email}")
    await update.message.reply_text("Validating your email...")
    try:
        response = requests.get(f'{API_BASE_URL}/clients/validate_email/?email={email}')
        logging.info(f"API response status code: {response.status_code}")
        logging.info(f"API response content: {response.content}")
        if response.status_code == 200 and response.json().get('status') == 'success':
            logging.info("Email validation successful, transitioning to PAYMENT_METHOD state.")
            client_data = response.json().get('client_data')
            if client_data:
                context.user_data['client_id'] = client_data.get('id')
                context.user_data['client_name'] = client_data.get('name')
                context.user_data['client_email'] = client_data.get('email')
                context.user_data['client_phone'] = client_data.get('phone_number')
                context.user_data['client_city'] = client_data.get('city')
                context.user_data['client_address'] = client_data.get('address')

                await update.message.reply_text("Email successfully validated! Please choose the payment method:")

                keyboard = [
                    [InlineKeyboardButton("Pix", callback_data='pix_payment')],
                    [InlineKeyboardButton("Pay on delivery", callback_data='pay_on_delivery')],
                    [InlineKeyboardButton("Back to Start", callback_data="start")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text("Choose the payment method:", reply_markup=reply_markup)
                
                return PAYMENT_METHOD_CHOICE
            else:
                logging.error("Client data is missing in the API response.")
                await update.message.reply_text("An error occurred while retrieving client data. Please try again later.")
                return CUSTOMER_REGISTRATION
        else:
            logging.info("Email validation failed, transitioning to CUSTOMER_REGISTRATION state.")
            await update.message.reply_text("Email not found. Please provide your details for registration (Name, Email, Phone, City, Address):")
            return CUSTOMER_REGISTRATION
    except Exception as e:
        logging.error(f"Exception during email validation: {e}")
        await update.message.reply_text("An error occurred during email validation. Please try again later.")
        return CUSTOMER_REGISTRATION

async def new_customer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the new customer callback query."""
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Please provide your details for registration (Name, Email, Phone, City, Address):")
    return CUSTOMER_REGISTRATION

async def customer_registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the customer registration message."""
    logging.info("Starting customer registration process.")
    customer_data = update.message.text.split(',')
    if len(customer_data) != 5:
        await update.message.reply_text("Invalid input format. Please provide your details in the format: Name, Email, Phone, City, Address")
        return CUSTOMER_REGISTRATION

    data = {
        "name": customer_data[0].strip(),
        "email": customer_data[1].strip(),
        "phone_number": customer_data[2].strip(),
        "city": customer_data[3].strip(),
        "address": customer_data[4].strip()
    }
    logging.info(f"Customer data: {data}")

    await update.message.reply_text("Registering your details...")
    try:
        response = requests.post(f'{API_BASE_URL}/clients/create/', json=data)
        logging.info(f"API response status code: {response.status_code}")
        logging.info(f"API response content: {response.content}")
        if response.status_code == 201:
            await update.message.reply_text("Registration successful! Please choose the payment method:")
            keyboard = [
                [InlineKeyboardButton("Pix", callback_data='pix_payment')],
                [InlineKeyboardButton("Pay on delivery", callback_data='pay_on_delivery')],
                [InlineKeyboardButton("Back to Start", callback_data="start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("Choose the payment method:", reply_markup=reply_markup)
            
            return PAYMENT_METHOD_CHOICE        
        else:
            await update.message.reply_text("Registration failed. Please try again.")
            return CUSTOMER_REGISTRATION
    except Exception as e:
        logging.error(f"Exception during registration: {e}")
        await update.message.reply_text("An error occurred during registration. Please try again later.")
        return CUSTOMER_REGISTRATION

async def payment_method(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the payment method callback query."""
    query = update.callback_query
    if query is None:
        logging.error("Callback query is None.")
        return PAYMENT_METHOD
    
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("Pix", callback_data='pix_payment')],
        [InlineKeyboardButton("Pay on delivery", callback_data='pay_on_delivery')],
        [InlineKeyboardButton("Back to Start", callback_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    logging.info("Displaying payment method options.")
    
    try:
        await query.edit_message_text("Choose the payment method:", reply_markup=reply_markup)
        logging.info("Payment method options displayed successfully.")
    except Exception as e:
        logging.error(f"Error displaying payment method options: {e}")
    
    return PAYMENT_METHOD_CHOICE

async def payment_method_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle user selection of a payment method."""
    query = update.callback_query
    await query.answer()

    if query.data == 'pix_payment':
        await query.edit_message_text("You chose Pix. Proceeding to the next step.")
        logging.info("Pix payment selected.")
        return ORDER_CONFIRMATION  # Change to the next relevant state

    elif query.data == 'pay_on_delivery':
        await query.edit_message_text("You chose pay on delivery. Proceeding to the next step.")
        logging.info("Pay on delivery selected.")
        return ORDER_CONFIRMATION  # Change to the next relevant state

    else:
        await query.edit_message_text("Invalid option. Please choose again.")
        return PAYMENT_METHOD_CHOICE  # Return to the same state in case of error
    
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
    
    # Generate the payload and QR Code using the Payload class
    payload = Payload(receiver_name, pix_key, f"{total:.2f}", city, txid)
    payload.gerarPayload()
    
    # Load the generated QR Code image
    qr_code_path = os.path.expanduser(os.path.join(payload.diretorioQrCode, 'pixqrcodegen.png'))
    with open(qr_code_path, 'rb') as qr_code_file:
        await query.message.reply_photo(photo=InputFile(qr_code_file), caption=f"Use the QR Code below to pay R$ {total:.2f} via Pix.")
    
    await query.message.reply_text("After completing the payment, please send the payment receipt.")
    logging.info("Pix payment selected and QR Code sent.")

async def pay_on_delivery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the pay on delivery callback query."""
    query = update.callback_query
    await query.answer()
    context.user_data['payment_method'] = 'pay_on_delivery'
    await query.message.reply_text("You chose pay on delivery. Your order will be processed and you can pay upon delivery.")
    logging.info("Pay on delivery selected.")
    await confirm_order(update, context)

async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ask for order confirmation."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Please confirm your order:")

    keyboard = [
        [InlineKeyboardButton("Confirm Order", callback_data='confirm_order_final')],
        [InlineKeyboardButton("Cancel Order", callback_data='cancel_order')]
        [InlineKeyboardButton("Back to Start", callback_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Do you want to confirm your order?", reply_markup=reply_markup)

async def cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the cancel order callback query."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Your order has been cancelled.")
    
async def talk_to_agent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the talk to agent callback query."""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        text="An agent will contact you soon."
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
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

async def confirm_order_final(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the final confirmation of the order."""
    await finalize_order(update, context)

def setup_handlers(application):
    """Setup all handlers for the application."""
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            EMAIL_VALIDATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, email_validation)],
            NEW_CUSTOMER: [MessageHandler(filters.TEXT & ~filters.COMMAND, new_customer)],
            CUSTOMER_REGISTRATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, customer_registration)],
            PAYMENT_METHOD: [CallbackQueryHandler(payment_method, pattern='^payment_method$')],
            PAYMENT_METHOD_CHOICE: [CallbackQueryHandler(payment_method_choice, pattern='^(pix_payment|pay_on_delivery)$')],
            ORDER_CONFIRMATION: [MessageHandler(filters.PHOTO, order_confirmation)],
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
    application.add_handler(CallbackQueryHandler(payment_method_choice, pattern='^(pix_payment|pay_on_delivery)$'))
    application.add_handler(CallbackQueryHandler(cancel, pattern='^cancel$'))
    application.add_handler(CallbackQueryHandler(confirm_order, pattern='^confirm_order$'))
    application.add_handler(CallbackQueryHandler(finalize_order, pattern='^finalize_order$'))
    application.add_handler(CallbackQueryHandler(confirm_order_final, pattern='^confirm_order_final$'))  # Adicione esta linha
    application.add_handler(CallbackQueryHandler(create_order, pattern='^create_order$'))
    application.add_handler(CallbackQueryHandler(create_order_item, pattern='^create_order_item$'))

def add_message_handlers(application):
    """Add all message handlers."""
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex(r'^[^,]+,[^,]+,[^,]+,[^,]+,[^,]+$'), customer_registration))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, email_validation))
    application.add_handler(MessageHandler(filters.PHOTO, order_confirmation))
    application.add_handler(MessageHandler(filters.COMMAND, start))