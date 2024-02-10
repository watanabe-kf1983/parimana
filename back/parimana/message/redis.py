from dataclasses import dataclass
import os

import redis

REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_DB_ID = 0

uri: str = f"redis://{REDIS_HOSTNAME}:{REDIS_PORT}/{REDIS_DB_ID}"


def createClient() -> redis.Redis:
    r = redis.Redis(host=REDIS_HOSTNAME, port=REDIS_PORT, db=REDIS_DB_ID)
    r.ping()    
    return r

@dataclass
class Subscribe:
    pubsub: redis.client.PubSub

    def listen(self):
        for msg in self.pubsub.listen():
            if msg["type"] == "message":
                msgstr = msg["data"].decode()
                if msgstr == "finished":
                    self.pubsub.unsubscribe()
                    break
                yield msgstr


class Channel:
    def __init__(self, name: str):
        self.name: str = name
        self.client: redis.Redis = createClient()

    def close(self) -> None:
        self.publish("finished")

    def publish(self, message: str) -> None:
        self.client.publish(f"channel-{self.name}", message)

    def subscribe(self) -> Subscribe:
        ps = self.client.pubsub()
        ps.subscribe(f"channel-{self.name}")
        return Subscribe(ps)
