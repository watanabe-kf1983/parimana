from datetime import timedelta
from parimana.tasks.base import route_task

event_serializer = "pickle"
task_serializer = "pickle"

result_serializer = "pickle"
result_expires = timedelta(minutes=60)
accept_content = ["application/json", "application/x-python-serialize"]

task_routes = (route_task,)
task_default_queue = "default"

broker_transport_options = {"visibility_timeout": 86400}  # 24 hours
