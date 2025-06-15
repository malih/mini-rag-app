from fastapi import FastAPI, APIRouter
import os

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)

# def welcome():
#     return {"message": "Welcome to the FastAPI application!"}
@base_router.get("/")
async def welcome():
    app_name = os.getenv("APP_NAME")
    app_version = os.getenv("APP_VERSION")
    print(f"App Name: {app_name}, App Version: {app_version}")
    return {
        "message": f"Welcome to {app_name} version {app_version}!",
        "documentation": "/docs",
        "redoc": "/redoc"
    }
