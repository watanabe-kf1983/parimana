from datetime import timedelta
import parimana.settings as settings

broker_url = settings.redis_db_uri
event_serializer = "pickle"
task_serializer = "pickle"

result_backend = settings.redis_db_uri
result_serializer = "pickle"
result_expires = timedelta(minute=60)
accept_content = ["application/json", "application/x-python-serialize"]
