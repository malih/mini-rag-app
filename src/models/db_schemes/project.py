from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId  

class Project(BaseModel):
    id: Optional[str] = None 
    Project_id: str = Field(..., min_length=1)

    @validator('Project_id')
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError('Invalid project_id format')
        return value