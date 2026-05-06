from fastapi import FastAPI
from contextlib import asynccontextmanager

from sqlmodel import SQLModel

from core.database import engine

# import all models (IMPORTANT for table creation)
from models import user, role, permission, mapping

from controller.user_controller import router as user_router
from controller.auth_controller import router as auth_router
from controller.role_controller import router as role_router
from controller.permission_controller import router as permission_router


# Lifespan (startup/shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    SQLModel.metadata.create_all(engine)
    yield
    # (optional) cleanup here


# App instance
app = FastAPI(
    title="IAM Service",
    version="1.0.0",
    lifespan=lifespan
)


# Include routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(role_router)
app.include_router(permission_router)


#Health check
@app.get("/")
def root():
    return {"message": "IAM Service is running"}