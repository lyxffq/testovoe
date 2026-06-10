def calculate_total_price(items: list) -> float:
    return sum(
        item.price * item.quantity
        for item in items
    )

def order_to_dict(order):
    return {
        "id": order.id,
        "user_id": order.user_id,
        "items": order.items,
        "total_price": order.total_price,
        "status": order.status.value,
        "created_at": str(order.created_at),
    }