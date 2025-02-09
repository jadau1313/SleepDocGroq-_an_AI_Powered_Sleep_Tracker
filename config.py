import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "Shadow123")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(base_dir, 'instance', 'sleep_tracker.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
