from pydantic import BaseModel

class JEAuthRequest(BaseModel):
    user: str
    password: str

class JEAuthResponse(BaseModel):
    status: str
    je_id: str

class JEPollingRequest(BaseModel):
    je_id: str
    status: str = "ready"
    current_task: str = None
    ping: float = None