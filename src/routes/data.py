from fastapi import APIRouter, Depends,FastAPI,uploadFile
import os
from controllers import DataController
from helpers.config import get_settings, Settings

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: uploadFile, app_settings: Settings = Depends(get_settings)):
    
    is_valid = DataController.validate_uploaded_file(file=file)
    return is_valid