from api.models.order_model import Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

def list_orders(page: int = 1, page_size: int = 10) -> dict:
    orders = Order.objects.all()
    paginator = Paginator(orders, page_size)
    
    try:
        orders_page = paginator.page(page)
    except PageNotAnInteger:
        orders_page = paginator.page(1)
    except EmptyPage:
        orders_page = paginator.page(paginator.num_pages)
    
    return {
        "orders": [{"id": order.id, "client": order.client, "status": order.status, "amount": order.amount} for order in orders_page],
        "total_pages": paginator.num_pages,
        "current_page": orders_page.number,
        "has_next": orders_page.has_next(),
        "has_previous": orders_page.has_previous()
    }