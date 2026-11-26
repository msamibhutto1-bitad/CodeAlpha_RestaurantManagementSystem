import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-insecure-key-change-me")
    DATABASE = os.environ.get("DATABASE", os.path.join(BASE_DIR, "restaurant.db"))
    DEBUG = os.environ.get("DEBUG", "1") == "1"
    ALLOWED_HOSTS = [h for h in os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost,testserver").split(",") if h]
    HOST = os.environ.get("HOST", "127.0.0.1")
    PORT = int(os.environ.get("PORT", 8000))
    TIME_ZONE = os.environ.get("TIME_ZONE", "UTC")
    RESERVATION_MINUTES = int(os.environ.get("RESERVATION_MINUTES", 90))
