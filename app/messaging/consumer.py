import asyncio
import json
import aio_pika

from app.config import settings
from app.workers.tasks import process_order
from app.workers.taskiq_broker import broker


async def main():
    await broker.startup()
    connection = await aio_pika.connect_robust(settings.RABBIT_URL)

    async with connection as con:
        channel = await con.channel()

        queue = await channel.declare_queue("new_order", durable=True)

        async with queue.iterator() as q:
            async for message in q:
                async with message.process():
                    data = json.loads(message.body)
                    order_id = data["order_id"]

                    print(f"[CONSUMER] received {order_id}")

                    await process_order.kiq(order_id)
                    


if __name__ == "__main__":
    asyncio.run(main())