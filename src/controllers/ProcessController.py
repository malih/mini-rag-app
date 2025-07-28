from .BaseController import BaseController
from .ProjectControllers import ProjectController
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os
import logging
from models import ProcessingEnum


class ProcessController(BaseController):
    """
    Controller for handling process-related operations.
    Inherits from BaseController to utilize common functionalities.
    """

    def __init__(self,project_id: str):

        super().__init__()
        self.project_id = project_id
        self.get_project_path = ProjectController().get_project_path(project_id=project_id)
    

    def get_file_extension(self, file_id: str):
        return os.path.splitext(file_id)[1]

    
    def get_file_loader(self, file_id: str):
        """
        Returns the appropriate file loader based on the file extension.
        """
        file_extension = self.get_file_extension(file_id)
        #
        file_path = os.path.join(self.get_project_path, file_id)
        
        if file_extension == ProcessingEnum.TXT.value:
            return TextLoader(file_path)
        elif file_extension == ProcessingEnum.PDF.value:
            return PyMupdfLoader(file_path)
        elif file_extension == ProcessingEnum.DOCX.value:
            return TextLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    def get_file_content(self, file_id: str):   
        """
        Retrieves the content of the file using the appropriate loader.
        """
        loader = self.get_file_loader(file_id)
        documents = loader.load()
        return documents

    def process_file_content(self, file_content:list, file_id: str, chunk_size: int = 100, overlap_size: int = 20):
        """
        Processes the file content by splitting it into chunks.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len
        )

        file_content_texts = [
            rec.page_content 
            for rec in file_content
        ]

        file_content_metadata = [
            rec.metadata 
            for rec in file_content
        ]

        documents = [
        Document(page_content=rec.page_content, metadata=rec.metadata)
        for rec in file_content
        ]


        chunks = text_splitter.split_documents(documents)
        return chunks 



