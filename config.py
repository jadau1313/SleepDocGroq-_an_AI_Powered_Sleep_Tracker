import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "Shadow123")
    SQLALCHEMY_DATABASE_URI = "sqlite:////instance/sleep_tracker.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
