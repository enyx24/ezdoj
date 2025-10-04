# je_polling.py
import time
import requests
import subprocess
import os
from dotenv import load_dotenv
from logging import logging_config

logging_config()
load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
TOKEN = os.getenv("JE_TOKEN", "your_je_token")

def check_new_submission():
    try:
        resp = requests.get(f"{BACKEND_URL}/polling", headers={"Authorization": f"Bearer {TOKEN}"})
        if resp.status_code == 200 and resp.json().get("job"):
            return resp.json()["job"]
    except Exception as e:
        print("Polling error:", e)
    return None

def judge(submission):
    print("Judging", submission["id"])
    subprocess.run(["isolate", "--run", "--", "python3", "main.py"], check=False)

def main():
    while True:
        job = check_new_submission()
        if job:
            judge(job)
        time.sleep(2)

if __name__ == "__main__":
    main()
