from fastapi import FastAPI
from app.routers import health, users, submissions, login, signup, je_auth, problems
from app.db import models


#==== DB CONNECTION ====
from app.db.connect_db import get_conn
conn = get_conn()

app = FastAPI(title="ezdoj", version="0.1.0")

#==== ROUTES ====
app.include_router(health.router)
app.include_router(users.router)
app.include_router(submissions.router)
app.include_router(login.router)
app.include_router(signup.router)
app.include_router(je_auth.router)
app.include_router(problems.router)

#==== CLOSE DB CONNECTION ====
@app.on_event("shutdown")
def shutdown_event():
    from app.db.connect_db import close_db
    close_db(conn)