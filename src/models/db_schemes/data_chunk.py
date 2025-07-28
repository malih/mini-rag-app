from pydantic import BaseModel, Field
from typing import Optional, List

class DataChunk(BaseModel):
    id: Optional[str] 
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict
    chunk_order: int= Field(..., ge=0)
    chunck_project_id: object
    
    class Config:
        arbitrary_types_allowed = True  
