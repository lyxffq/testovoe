from app.tasks.broker import broker
import asyncio

@broker.task
async def process_order(order_id: str):
    await asyncio.sleep(2)
    print(f"Order {order_id} processed")