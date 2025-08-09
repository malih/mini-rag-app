from .BaseController import BaseController
from fastapi import HTTPException, UploadFile
from models import ResponseSignal
import os
import aiofile
from aiofile import AIOFile

class ProjectController(BaseController):
    def __init__(self):
        super().__init__()

    def get_project_path(self, project_id: str) -> str:
        """
        Returns the path to the project directory based on the project ID.
        """
        project_dir = os.path.join(self.file_dire, project_id)

        if not os.path.exists(project_dir):
            os.makedirs(project_dir)

        return project_dir