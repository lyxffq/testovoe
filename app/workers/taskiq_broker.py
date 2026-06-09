from taskiq_aio_pika import AioPikaBroker
from app.config import settings

broker = AioPikaBroker(settings.RABBIT_URL)

import app.workers.tasks
