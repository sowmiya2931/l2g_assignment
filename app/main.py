from fastapi import FastAPI
from routes.auth import auth_router
from routes.notes import notes_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(notes_router, prefix="/notes")

@app.get("/")
def root():
    return {"message": "Welcome to the Notes App API"}
