from fastapi import FastAPI
from sqlmodel import SQLModel
from app.core.database import engine
from app.controller.student_controller import router as student_router

app = FastAPI(title="Student Management API")


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


app.include_router(student_router)