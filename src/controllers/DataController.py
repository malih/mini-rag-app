from BaseController import BaseController
from fastapi import HTTPException, UploadFile

class DataController(BaseController):
    def __init__(self):
        super().__init__()


    def validate_uploaded_file(self, file):
        
        if file.content_type not in self.app_settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file.content_type}. Allowed types are: {', '.join(self.app_settings.ALLOWED_FILE_TYPES)}"
            )
        
        if file.size > self.app_settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds the maximum limit of {self.app_settings.MAX_FILE_SIZE} bytes."
            ) 

        return  {
            "status": "success",
            "message": "File is valid.",
            "file_name": file.filename,
            "content_type": file.content_type,
            "size": file.size
        }
        

