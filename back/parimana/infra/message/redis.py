from contextlib import asynccontextmanager
import os
from typing import AsyncGenerator
import asyncio

import redis
import redis.asyncio as aioredis
import async_timeout

REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_DB_ID = 0

uri: str = f"redis://{REDIS_HOSTNAME}:{REDIS_PORT}/{REDIS_DB_ID}"


_MSG_CLOSE = "*&*&*&*&finished*&*&*&*&"


class Channel:
    def __init__(self, name: str):
        self.name: str = name
        self.client: redis.Redis = redis.from_url(uri)
        self.aioclient: aioredis.Redis = aioredis.from_url(uri)

    def pingged(self) -> "Channel":
        self.client.ping()
        return self

    def close(self) -> None:
        self.publish(_MSG_CLOSE)

    def publish(self, message: str) -> None:
        self.client.publish(f"channel-{self.name}", message)

    @asynccontextmanager
    async def _asubcribe(self) -> aioredis.client.PubSub:
        async with self.aioclient.pubsub() as p:
            try:
                await p.subscribe(f"channel-{self.name}")
                yield p
            finally:
                await p.unsubscribe(f"channel-{self.name}")
                await p.aclose()

    async def alisten(self) -> AsyncGenerator[str, None]:
        async with self._asubcribe() as p:
            while True:
                async with async_timeout.timeout(60):
                    message = await p.get_message(ignore_subscribe_messages=True)
                    if message is not None:
                        msg = message["data"].decode()
                        if msg == _MSG_CLOSE:
                            break
                        else:
                            yield msg
                    await asyncio.sleep(0.01)
