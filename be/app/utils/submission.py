from app.db.connect_db import get_conn
from app.utils.logging import logging
from app import job_queue
conn = get_conn()
cursor = conn.cursor()

def submit(user, request):
    cursor.execute("SELECT id from users WHERE username = %s", (user,))
    user_id = cursor.fetchone()[0]
    cursor.execute(
        "INSERT INTO submissions (user_id, problem_id, code, language_id, status) VALUES (%s, %s, %s, %s, %s) RETURNING id, status",
        (user_id, request.problem_id, request.code, request.language_id, 'queued')    
    )
    try:
        conn.commit()
        job_queue.append(cursor.fetchone()[0])
    except Exception as e:
        conn.rollback()
        logging.error(f"Error occurred while submitting: {e}")
    submission = cursor.fetchone()
    return submission

def get_submission(submission_id):
    cursor.execute("SELECT id, problem_id, code, language_id, status FROM submissions WHERE id = %s", (submission_id,))
    return cursor.fetchone()