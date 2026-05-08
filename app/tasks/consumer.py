import asyncio
import json
import aio_pika

from app.config import settings
from app.tasks.tasks import process_order


async def main():
    connection = await aio_pika.connect_robust(
        settings.RABBIT_URL
    )

    async with connection as con:
        channel = await connection.channel()

        queue = await channel.declare_queue("new_order", durable = True)

        async with queue.iterator() as q:
            async for message in q:
                async with message.process():
                    data = json.loads(message.body)
                    order_id = data["order_id"]

                    await process_order.kiq(order_id)


if __name__ == "__main__":
    asyncio.run(main())