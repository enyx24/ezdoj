from app.db.connect_db import get_conn
from app.utils.logging import logging
from be.app.models.problem import ProblemRequest, TestUploadRequest
conn = get_conn()
cursor = conn.cursor()

def get_problem(problem_id):
    cursor.execute("SELECT * FROM problems WHERE id = %s", (problem_id,))
    problem = cursor.fetchone()
    if not problem:
        logging.error(f"Problem with id {problem_id} not found.")
        return None
    return problem

def set_problem(ProblemRequest):
    if (ProblemRequest.id):
        cursor.execute(
            """
            UPDATE problems
            SET title = %s,
                description = %s,
                difficulty = %s,
                tags = %s,
                is_active = %s,
                updated_at = CURRENT_TIMESTAMP,
                author_id = %s,
                attachments = %s,
                time_limit = %s,
                memory_limit = %s,
                language_restrictions = %s,
                test_id = %s
            WHERE id = %s
            """,
            (
                ProblemRequest.title,
                ProblemRequest.description,
                ProblemRequest.difficulty,
                ProblemRequest.tags,
                ProblemRequest.is_active,
                ProblemRequest.author_id,
                ProblemRequest.attachments,
                ProblemRequest.time_limit,
                ProblemRequest.memory_limit,
                ProblemRequest.language_restrictions,
                ProblemRequest.test_id,
            )
        )
        try:
            conn.commit()
            logging.info(f"Problem with id {ProblemRequest.id} updated successfully.")
            return ProblemRequest.id
        except Exception as e:
            conn.rollback()
            logging.error(f"Error occurred while updating problem: {e}")
            return None
    cursor.execute(
        """
        INSERT INTO problems (title, description, difficulty, tags, is_active, created_at, updated_at, author_id, attachments, time_limit, memory_limit, language_restrictions, test_id)
        VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, NULL, %s, %s, %s, %s, %s, %s) RETURNING id
        """,
        (
            ProblemRequest.title,
            ProblemRequest.description,
            ProblemRequest.difficulty,
            ProblemRequest.tags,
            ProblemRequest.is_active,
            ProblemRequest.author_id,
            ProblemRequest.attachments,
            ProblemRequest.time_limit,
            ProblemRequest.memory_limit,
            ProblemRequest.language_restrictions,
            ProblemRequest.test_id
        )
    )
    try:
        conn.commit()
        problem_id = cursor.fetchone()[0]
        logging.info(f"Problem created with id {problem_id}.")
        return problem_id
    except Exception as e:
        conn.rollback()
        logging.error(f"Error occurred while creating problem: {e}")
        return None

def get_test(test_id):
    cursor.execute("SELECT * FROM tests WHERE id = %s", (test_id,))
    problem = cursor.fetchone()
    if not problem:
        logging.error(f"Test with id {test_id} not found.")
        return None
    return problem

def set_test(TestUploadRequest):
    cursor.execute("INSERT INTO tests()")