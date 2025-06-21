from fastapi import FastAPI, APIRouter, Depends
from helpers.config import get_settings, Settings
import os

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)

# def welcome():
#     return {"message": "Welcome to the FastAPI application!"}
@base_router.get("/")
async def welcome(app_settings : Settings =Depends(get_settings)):
    
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION

    return {
        "message": f"Welcome to {app_name} version {app_version}!",
        "documentation": "/docs",
        "redoc": "/redoc"
    }
