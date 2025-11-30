from app.db.connect_db import get_conn
from app.utils.logging import logging
from app.models.problem import ProblemUploadRequest, TestUploadRequest
conn = get_conn()
cursor = conn.cursor()

def get_problem(problem_id: int):
    cursor.execute("SELECT * FROM problems WHERE id = %s", (problem_id,))
    problem = cursor.fetchone()
    if not problem:
        logging.error(f"Problem with id {problem_id} not found.")
        return None
    return problem

def set_problem(problem_request: ProblemUploadRequest):
    if problem_request.id:
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
                problem_request.title,
                problem_request.description,
                problem_request.difficulty,
                problem_request.tags,
                problem_request.is_active,
                problem_request.author_id,
                problem_request.attachments,
                problem_request.time_limit,
                problem_request.memory_limit,
                problem_request.language_restrictions,
                problem_request.test_id,
            )
        )
        try:
            conn.commit()
            logging.info(f"Problem with id {problem_request.id} updated successfully.")
            return problem_request.id
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
            problem_request.title,
            problem_request.description,
            problem_request.difficulty,
            problem_request.tags,
            problem_request.is_active,
            problem_request.author_id,
            problem_request.attachments,
            problem_request.time_limit,
            problem_request.memory_limit,
            problem_request.language_restrictions,
            problem_request.test_id
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

def get_test(test_id: int):
    cursor.execute("SELECT * FROM tests WHERE id = %s", (test_id,))
    problem = cursor.fetchone()
    if not problem:
        logging.error(f"Test with id {test_id} not found.")
        return None
    return problem

def set_test(test_request: TestUploadRequest):
    cursor.execute(
        """
        INSERT INTO tests (test_file_path, created_at, updated_at, author_id)
        VALUES (%s, CURRENT_TIMESTAMP, NULL, %s) RETURNING id
        """,
        (
            test_request.test_file_path,
            test_request.author_id,
        )
    )
    try:
        conn.commit()
        test_id = cursor.fetchone()[0]
        logging.info(f"Test created with id {test_id}.")
        return test_id
    except Exception as e:
        conn.rollback()
        logging.error(f"Error occurred while creating test: {e}")
        return None