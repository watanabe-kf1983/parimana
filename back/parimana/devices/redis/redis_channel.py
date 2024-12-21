from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncGenerator
import asyncio

import redis
import redis.asyncio as aioredis
import async_timeout

from parimana.utils.message import Channel, PublishCenter


_MSG_CLOSE = "*&*&*&*&finished*&*&*&*&"


class RedisChannel(Channel):
    def __init__(self, db_uri, channel_id: str):
        self.channel_id: str = channel_id
        self.client: redis.Redis = redis.from_url(db_uri)
        self.aioclient: aioredis.Redis = aioredis.from_url(db_uri)
        self.client.ping()

    def publish(self, message: str) -> None:
        self.client.publish(f"channel-{self.channel_id}", message)

    def close(self) -> None:
        self.publish(_MSG_CLOSE)

    @asynccontextmanager
    async def _asubcribe(self) -> aioredis.client.PubSub:
        async with self.aioclient.pubsub() as p:
            try:
                await p.subscribe(f"channel-{self.channel_id}")
                yield p
            finally:
                await p.unsubscribe(f"channel-{self.channel_id}")
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


@dataclass
class RedisChannelFactory:
    db_uri: str

    @property
    def publish_center(self):
        return PublishCenter(self.get_channel)

    def get_channel(self, channel_id) -> Channel:
        return RedisChannel(self.db_uri, channel_id)
