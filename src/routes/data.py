from fastapi import APIRouter, Depends,FastAPI,UploadFile,Request
import os
from fastapi.responses import JSONResponse , FileResponse
from controllers import DataController, ProjectController,ProcessController
from helpers.config import get_settings, Settings
import logging
import aiofile
from aiofile import AIOFile
from .schemes.data import ProcessRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schemes import DataChunk, Asset
from models.AssetModel import AssetModel
from models.enums.AssetTypeEnum import AssetTypeEnum
from models.enums.ResponseEnum   import ResponseSignal


logger= logging.getLogger('unicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(request:Request,project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):

    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)
    

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
    
    except Exception as e:

        logger.error(f"Failed to upload file: {str(e)}")
        print(str(e))  # Affiche l'erreur dans le terminal
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Failed to upload file: {str(e)}"
            }
        )
    
    #store the asset in the database
    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)

    #create the asset record
    asset_resource = Asset(
        asset_project_id=project.id,
        asset_type=AssetTypeEnum.FILE.value,
        asset_name=file_id,
        asset_size=os.path.getsize(file_path)
    )

    asset_record = await asset_model.create_asset(asset=asset_resource)
        

    return JSONResponse(
        content={
            "signnal":ResponseSignal.SUCCESS.value,
            "file_id": str(asset_record.id),
        }
    )
    
 

@data_router.post("/process/{project_id}")
async def process_endpoint(request:Request , project_id:str,process_request: ProcessRequest):
    
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset

    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)

    chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)

    if do_reset==1:
       _=await chunk_model.delete_chunks_by_project_id(project_id=project.id)

    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)

    project_file_ids = {}
    if process_request.file_id:
        asset_record = await asset_model.get_asset_record(
            asset_project_id=project.id,
            asset_name=process_request.file_id
        )

        if asset_record is None:
            return JSONResponse(
                status_code=400,
                content={
                    "signal": ResponseSignal.NO_FILE_ERROR.value,
                }
            )
        
        project_file_ids = {
            asset_record.id: asset_record.asset_name
        }

    else:

        project_files = await asset_model.get_all_project_assets(
            asset_project_id=project.id,
            asset_type=AssetTypeEnum.FILE.value,
            asset_name=project.name
        )

        project_file_ids = {
            record.id: record.asset_name
            for record in project_files
        }
    
    if len(project_file_ids) == 0:
        return JSONResponse(
            status_code=400,
            content={
                "signal": ResponseSignal.NO_FILE_ERROR.value,
            }
        )

    process_controller = ProcessController(project_id=project_id)
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    no_records = 0
    no_files = 0
    for asset_id, file_id in project_file_ids.items():
        
        file_content = process_controller.get_file_content(file_id=file_id) 

        if file_content is None:
            logger.error(f"File {file_id} not found in project {project_id}.")
            continue

        file_chunks = process_controller.process_file_content(
            file_content=file_content,
            file_id=file_id,    
            chunk_size=chunk_size,
            overlap_size=overlap_size
        )
        if file_chunks is None or len(file_chunks) == 0:
            logger.warning(f"No content to process for file {file_id}.")
            continue 
        
        file_chunks_records = [
            DataChunk(
                chunk_text=chunk.page_content,
                chunk_metadata=chunk.metadata,
                chunk_order=i+1,
                chunck_project_id=project.id,
                chunk_asset_id=asset_id
            )
            for i,chunk in enumerate(file_chunks)

        ]
                    
        chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)

        no_records = await chunk_model.insert_many_chunks(
        chunks=file_chunks_records)
        no_files += 1

    return JSONResponse(
        content={
            "signal": ResponseSignal.SUCCESS.value,
            "Inserted_chunks": no_records,
            "processed_files": no_files
        }
    )