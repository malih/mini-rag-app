from pydantic import BaseModel, Field
from typing import Optional, List
from bson import ObjectId

class DataChunk(BaseModel):
    id: Optional[str] = Field(None, alias="_id") 
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict
    chunk_order: int= Field(..., ge=0)
    chunck_project_id: object
    chunk_asset_id: ObjectId

    class Config:
        arbitrary_types_allowed = True  

    @classmethod
    def get_indexes(cls):
        return [
            {
                "key": [("chunck_project_id", 1)],
                "unique": False,
                "name": "chunk_project_id_index"
            }
        ]
