from pydantic import BaseModel

class SubmissionRequest(BaseModel):
    problem_id: int
    code: str
    language_id: int
    token: str

class SubmissionResponse(BaseModel):
    # status_code: int
    submission_id: int
    status: str
    message: str | None = None
