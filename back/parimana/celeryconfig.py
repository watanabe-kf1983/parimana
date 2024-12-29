from datetime import timedelta
import parimana.settings as settings

broker_url = settings.REDIS_DB_URI
event_serializer = "pickle"
task_serializer = "pickle"

result_backend = settings.REDIS_DB_URI
result_serializer = "pickle"
result_expires = timedelta(minutes=60)
accept_content = ["application/json", "application/x-python-serialize"]
