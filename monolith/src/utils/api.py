from ..models.task_model import Task
from ..models.user_model import User


def user_serializer(users: list[User]):
    return [{"uuid":user.id,"first_name":user.first_name,"last_name":user.last_name,"email":user.email} for user in users]


def single_user_serializer(user: User):
    # If user is None, return None so callers can decide how to handle 404
    if not user:
        return None

    return {"uuid": user.id, "first_name": user.first_name, "last_name": user.last_name, "email": user.email}


def task_serializer(tasks: list[Task]):
    return [{"id":task.id,"first_name":task.task,"last_name":task.task_description,"conclusion":task.task_conclusion, "user_id":task.user_id} for task in tasks]


def single_task_serializer(task: Task):
    return {"id":task.id,"first_name":task.task,"last_name":task.task_description,"conclusion":task.task_conclusion}
