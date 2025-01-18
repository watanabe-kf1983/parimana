from parimana.context import context as cx
from parimana.tasks.analyse import AnalyseTaskOptions


def handler(event, context):
    command_name = event["command"]
    args = event.get("args", [])
    kwargs = event.get("kwargs", {})

    if command_name in commands:
        return commands[command_name](*args, **kwargs)
    else:
        available = ", ".join(commands.keys())
        raise ValueError(
            f"Illegal command name: {command_name}. Legal commands are: [{available}]"
        )


commands = {}


def command(func):
    commands[func.__name__] = func
    return func


@command
def start_analyse(*args, **kwargs):
    options = AnalyseTaskOptions(*args, **kwargs)
    task_id = cx.analyse_tasks.scrape_and_analyse(options).delay().id
    return {"task_id": task_id}
