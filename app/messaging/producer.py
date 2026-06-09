import json
import aio_pika

from app.config import settings

async def publish_new_order(order_id: str):
    connection = await aio_pika.connect_robust(
        settings.RABBIT_URL
    )

    async with connection as con:
        channel = await con.channel()

        queue = await channel.declare_queue(
            "new_order",
            durable=True
        )

        message = aio_pika.Message(
            body=json.dumps(
                {"order_id": order_id}
            ).encode()
        )

        await channel.default_exchange.publish(
            message,
            routing_key=queue.name
        )