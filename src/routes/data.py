from fastapi import APIRouter, Depends,FastAPI,UploadFile
import os
from fastapi.responses import JSONResponse 
from controllers import DataController, ProjectController,ProcessController
from helpers.config import get_settings, Settings
import logging
import aiofile
from aiofile import AIOFile
from .schemes.data import ProcessRequest


logger= logging.getLogger('unicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    

    data_controller = DataController()
    is_valid = data_controller.validate_uploaded_file(file=file)
    
    if not is_valid:
        return JSONResponse(
            status_code=400,
            content={
            "status": "error",
            "message": "Invalid file."
        })
    project_controller = ProjectController()
    project_dir_path = project_controller.get_project_path(project_id=project_id)
    file_path, file_id = data_controller.generate_unique_filepath(orig_file_name=file.filename, project_id=project_id)
    # Ajoute ceci pour créer le dossier parent si besoin
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        async with AIOFile(file_path, 'wb') as out_file:
            while chunk :=await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await out_file.write(chunk)
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "File uploaded successfully.",
                "file_name": file.filename,
                "file_path": file_path,
                "file_id": file_id
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
 

@data_router.post("/process/{project_id}")
async def process_endpoint(project_id:str,process_request: ProcessRequest):
    file_id = process_request.file_id

    process_controller = ProcessController(project_id=project_id)
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    file_content = process_controller.get_file_content(file_id=file_id) 
    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,    
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )
    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "No content to process."
            }
        ) 
    else :
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "File processed successfully.",
                "file_id": file_id,
                "chunks": [
                    {
                        "page_content": chunk.page_content,
                        "metadata": chunk.metadata
                    }
                    for chunk in file_chunks
                ]
            }
        )
                

    return file_id