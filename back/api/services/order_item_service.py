from api.models.order_item_model import OrderItem, Order, Item

def create_order_item(order_id: int, item_id: int, quantity: int) -> OrderItem:
    order = Order.objects.get(id=order_id)
    item = Item.objects.get(id=item_id)
    order_item = OrderItem(order=order, item=item, quantity=quantity)
    order_item.save()
    return order_item

def get_order_item_by_id(order_item_id: int) -> OrderItem:
    return OrderItem.objects.get(id=order_item_id)

def update_order_item(order_item_id: int, quantity: int = None) -> OrderItem:
    order_item = OrderItem.objects.get(id=order_item_id)
    if quantity is not None:
        order_item.quantity = quantity
    order_item.save()
    return order_item

def delete_order_item(order_item_id: int) -> None:
    order_item = OrderItem.objects.get(id=order_item_id)
    order_item.delete()

def list_order_items_by_order(order_id: int) -> list:
    order = Order.objects.get(id=order_id)
    return list(OrderItem.objects.filter(order=order))