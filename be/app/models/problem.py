from pydantic import BaseModel

class ProblemUploadRequest(BaseModel):
    """
    Model for uploading a problem.
    Attributes:
        id: The unique identifier of the problem.
        title: The title of the problem.
        description: The description of the problem. Can be markdown formatted.
        difficulty: The difficulty level of the problem (e.g., 'easy', 'medium', 'hard').
        tags: A list of tags associated with the problem.
        is_active: A boolean indicating if the problem is active.
        created_at: The timestamp when the problem was created.
        updated_at: The timestamp when the problem was last updated.
        author_id: The unique identifier of the author who created the problem.
        attachments: A list of attachment URLs or file paths associated with the problem.
        time_limit: The time limit for solving the problem in seconds.
        memory_limit: The memory limit for solving the problem in megabytes.
        language_restrictions: A list of programming languages allowed for solving the problem. If none, there's no restriction.
        test_id: The unique identifier of the test associated with the problem.
    """
    id: int
    title: str
    description: str
    solution: str | None = None
    code_solution: str | None = None
    difficulty: str
    tags: list[str]
    is_active: bool = True
    created_at: str
    updated_at: str | None = None
    author_id: int
    attachments: list[str] | None = None
    time_limit: float | None = None
    memory_limit: int | None = None
    language_restrictions: list[str] | None = None
    test_id: int | None = None

class ProblemUploadResponse(BaseModel):
    id: int
    status: str
    message: str | None = None

    
class TestUploadRequest(BaseModel):
    """
        Model for uploading a test case.
        
        Attributes:
            id: Unique identifier for the test case.
            test_file_path: Path to the test file. Test file needs to be a zip file.
            created_at: Timestamp when the test case was created.
            updated_at: Timestamp when the test case was last updated.
            author_id: Unique identifier for the author of the test case.
    """
    id: int
    test_file_path: str | None = None
    created_at: str
    updated_at: str | None = None
    author_id: int

class TestUploadResponse(BaseModel):
    id: int
    status: str
    message: str | None = None