from pydantic import BaseModel

class SubmissionRequest(BaseModel):
    """
    Model for submission request data.
    Attributes:
        problem_id: ID of the problem being submitted.
        code: The source code being submitted.
        language_id: ID of the programming language used.
        token: Authentication token of the user submitting the code.
    """
    problem_id: int
    code: str
    language_id: int
    token: str

class SubmissionResponse(BaseModel):
    # status_code: int
    submission_id: int
    status: str
    message: str | None = None
