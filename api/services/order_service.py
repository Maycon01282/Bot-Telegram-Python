from api.models.order_model import Order

def create_order(client: str, status: str, amount: float) -> Order:
    if status not in Order.Status.values:
        raise ValueError(f"Invalid status value: {status}")
    order = Order(client=client, status=status, amount=amount)
    order.save()
    return order

def get_order_by_id(order_id: int) -> Order:
    return Order.objects.get(id=order_id)

def update_order(order_id: int, client: str = None, status: str = None, amount: float = None) -> Order:
    order = Order.objects.get(id=order_id)
    if client:
        order.client = client
    if status:
        if status not in Order.Status.values:
            raise ValueError(f"Invalid status value: {status}")
        order.status = status
    if amount:
        order.amount = amount
    order.save()
    return order

def delete_order(order_id: int) -> None:
    order = Order.objects.get(id=order_id)
    order.delete()

def list_orders_by_client(client: str) -> list:
    return list(Order.objects.filter(client=client))

def list_orders() -> list:
    return list(Order.objects.all())