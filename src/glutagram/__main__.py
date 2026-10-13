import asyncio
from functools import partial
from random import random

import anyio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from glutagram import jobs
from glutagram.config import config
from glutagram.storage import Storage


async def async_main() -> None:
    scheduler = AsyncIOScheduler()

    for chat_id, chat in config.chats.items():
        # base + (0..15)
        interval = chat.interval + (random() * 15.0)

        storage = Storage(f"storages/history_{chat_id}.pickle")

        scheduler.add_job(partial(jobs.gather, storage, chat_id, chat), IntervalTrigger(seconds=interval))
        print(f"registered chat {chat_id} at interval {interval}")

    scheduler.start()

    try:
        await anyio.sleep_forever()
    except (asyncio.CancelledError, KeyboardInterrupt):
        pass


if __name__ == "__main__":
    asyncio.run(async_main())
