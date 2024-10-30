from api.models.product_model import Product
from django.core.exceptions import ObjectDoesNotExist

def list_products():
    products = Product.objects.all()
    return [{"id": product.id, "category": product.category, "photo_url": product.photo_url, "name": product.name, "description": product.description, "price": product.price} for product in products]

def get_product_by_id(product_id):
    try:
        product = Product.objects.get(id=product_id)
        return {"id": product.id, "category": product.category, "photo_url": product.photo_url, "name": product.name, "description": product.description, "price": product.price}
    except ObjectDoesNotExist:
        return None

def create_product(data):
    product = Product.objects.create(
        category=data['category'],
        photo_url=data['photo_url'],
        name=data['name'],
        description=data['description'],
        price=data['price']
    )
    return {"id": product.id, "category": product.category, "photo_url": product.photo_url, "name": product.name, "description": product.description, "price": product.price}

def update_product(product_id, data):
    try:
        product = Product.objects.get(id=product_id)
        product.category = data.get('category', product.category)
        product.photo_url = data.get('photo_url', product.photo_url)
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.save()
        return {"id": product.id, "category": product.category, "photo_url": product.photo_url, "name": product.name, "description": product.description, "price": product.price}
    except ObjectDoesNotExist:
        return None

def delete_product(product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        return True
    except ObjectDoesNotExist:
        return False
