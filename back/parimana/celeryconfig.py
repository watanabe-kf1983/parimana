from datetime import timedelta
from parimana.settings import Settings

settings = Settings()

broker_url = settings.redis_uri
event_serializer = "pickle"
task_serializer = "pickle"

result_backend = settings.redis_uri
result_serializer = "pickle"
result_expires = timedelta(minutes=60)
accept_content = ["application/json", "application/x-python-serialize"]
