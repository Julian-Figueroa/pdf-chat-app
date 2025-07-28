import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SESSION_PERMANENT = True
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
    UPLOAD_URL = os.environ["UPLOAD_URL"]
    # "broker_url": os.environ.get("REDIS_URI", False),
    CELERY = {
        "broker_url": "redis://localhost:6379/0",  # Key should be broker_url, not broker
        "result_backend": "redis://localhost:6379/0",  # Key should be result_backend, not backend
        "task_ignore_result": True,
        "broker_connection_retry_on_startup": True,
        "task_serializer": "json",
        "result_serializer": "json",
        "accept_content": ["json"],
        "timezone": "UTC",
        "enable_utc": True,
    }
