from fastapi import APIRouter, Depends,FastAPI,uploadFile
import os
from fastapi.responses import JSONResponse 
from controllers import DataController, ProjectController
from helpers.config import get_settings, Settings
import logging


logger= logging.getLogger('unicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: uploadFile, app_settings: Settings = Depends(get_settings)):
    

    data_controller = DataController()
    is_valid = data_controller.validate_uploaded_file(file=file)
    
    if not is_valid:
        return JSONResponse(
            status_code=400,
            content={
            "status": "error",
            "message": "Invalid file."
        })

    project_dir_path = ProjectController.get_project_path(project_id=project_id)
    file_path = data_controller.generate_unique_file_name(orig_file_name=file.filename, project_id=project_id)

    try:
        async with aiofile.open(file_path, 'wb') as out_file:
            while chunk :=await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await out_file.write(chunk)
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "File uploaded successfully.",
                "file_name": file.filename,
                "file_path": file_path
            }
        )
    except Exception as e:

        logger.error(f"Failed to upload file: {str(e)}")

        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Failed to upload file: {str(e)}"
            }
        )
 
