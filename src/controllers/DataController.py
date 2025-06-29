from .BaseController import BaseController
from fastapi import HTTPException, UploadFile
from models import ResponseSignal
from .ProjectControllers import ProjectController
import re,os


class DataController(BaseController):
    def __init__(self):
        super().__init__()


    def validate_uploaded_file(self, file):
        
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file.content_type}. Allowed types are: {', '.join(self.app_settings.FILE_ALLOWED_TYPES)}"
            )
        
        if file.size > self.app_settings.FILE_MAX_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds the maximum limit of {self.app_settings.FILE_MAX_SIZE} bytes."
            ) 

        return  {
            "status": ResponseSignal.SUCCESS.value,
            "message": "File is valid.",
            "file_name": file.filename,
            "content_type": file.content_type,
            "size": file.size
        }

    def generate_unique_filepath(self, orig_file_name:str, project_id: str):
        
        random_key= self.generate_random_string(10)
        project_controller = ProjectController()
        project_path = project_controller.get_project_path(project_id=project_id)

        cleaned_file_name = self.get_cleaned_file_name(orig_file_name)

        new_file_path = os.path.join(project_path, f"{cleaned_file_name}_{random_key}")

        while os.path.exists(new_file_path):
            random_key = self.generate_random_string(10)
            new_file_path = os.path.join(project_path, f"{cleaned_file_name}_{random_key}")

        return new_file_path,random_key+"_"+cleaned_file_name

    def get_cleaned_file_name(self, file_name: str) -> str:
        """
        Cleans the file name by removing spaces and special characters.
        """
        cleaned_file_name = re.sub(r'[^\w\-\.]', '_', file_name).strip('_')
        return cleaned_file_name


