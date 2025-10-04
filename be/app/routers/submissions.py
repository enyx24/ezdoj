from fastapi import APIRouter
from app.models.submission import SubmissionResponse, SubmissionRequest
from app.utils.auth import get_current_user
from app.utils.submission import submit

router = APIRouter(prefix="/submissions", tags=["submissions"])

@router.post("/submit")
def create_submission(request: SubmissionRequest, response: SubmissionResponse):
    # response.status_code = 200

    user = get_current_user(request.token)
    if user == None:
        # response.status_code = 401
        return {"error": "Unauthorized"}

    submission = submit(user, request)
    # print(submission)
    if not submission:
        # response.status_code = 400
        return {"error": "Submission failed. Try again later."}

    response.submission_id = submission[0]
    response.status = submission[1]
    return response