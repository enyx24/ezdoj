from dotenv import load_dotenv
load_dotenv("app/.env")
from app.utils.logging import logging_config
logging_config()