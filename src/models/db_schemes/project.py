from pydantic import BaseModel, Field, ConfigDict, validator
from typing import Optional
from bson.objectid import ObjectId

class Project(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    Project_id: str = Field(..., min_length=1)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @validator('Project_id')
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError('Invalid project_id format')
        return value
    
    class config:
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
        return [
            {
                "key": [("Project_id", 1)],
                "unique": True,
                "name": "project_id_index"
            }
        ]