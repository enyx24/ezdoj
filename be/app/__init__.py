from dotenv import load_dotenv
load_dotenv("app/.env")
from app.utils.logging import logging_config
logging_config()

active_judges = {}

from collections import deque
job_queue = deque()