from pathlib import Path
from typing import List
import pandas as pd
from PIL import Image
import pytesseract
from langchain.docstore.document import Document
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    CSVLoader,
)
from src.logging import Logger


class Ingestion: 

    def __init__(self):
        self.logger = Logger()
        if self.logger:
            self.logger.log_system("info", "Logger object initialized successfully")
        else:
            self.logger.log_system("error", "Logger object failed to initialize")


    def load_documents_from_dir(self, directory_path: str, file_types: List[str]) -> List[Document]:
        """
        Loads documents from a directory using LangChain loaders and pandas for Excel.

        Args:
            directory_path (str): Path to directory containing files.
            file_types (List[str]): List of allowed file extensions.

        Returns:
            List[Document]: A list of LangChain Document objects.
        """
        self.logger.log_system("info", f"Starting to load documents from: {directory_path}")
        supported_images = {'.png', '.jpg', '.jpeg'}
        documents = []

        for file_path in Path(directory_path).rglob("*"):
            file_ext = file_path.suffix.lower()

            try:
                self.logger.log_system("info", f"Processing file: {file_path}")
                if file_ext not in file_types and file_ext not in supported_images:
                    continue

                loader = None
                docs = []

                if file_ext == '.txt':
                    loader = TextLoader(str(file_path), autodetect_encoding=True)
                    docs = loader.load()

                elif file_ext == '.pdf':
                    loader = PyPDFLoader(str(file_path))
                    docs = loader.load()

                elif file_ext == '.xlsx':
                    df = pd.read_excel(file_path)
                    content = df.to_string(index=False)
                    doc = Document(page_content=content, metadata={"source": str(file_path)})
                    docs = [doc]

                elif file_ext == '.csv':
                    loader = CSVLoader(str(file_path))
                    docs = loader.load()

             
                elif file_ext in supported_images:
    
                    try:
                        self.logger.log_system("info" , "starting to decode the image")
                        image = Image.open(file_path)
                        text = pytesseract.image_to_string(image)
                        doc = Document(page_content=text, metadata={"source": str(file_path)})
                        docs = [doc]
                    
                    except Exception as img_error:
                        self.logger.log_system("error", f"Image OCR failed for {file_path}: {img_error}")
                        continue

                else:
                    self.logger.log_system("warning", f"Unsupported file format: {file_path}")
                    continue

                documents.extend(docs)
                self.logger.log_system("info", f"Loaded {len(docs)} documents from {file_path}")

            except Exception as e:
                self.logger.log_system("error", f"Skipped file {file_path} due to error: {e}")

        self.logger.log_system("info", f"Total documents loaded: {len(documents)}")
        return documents


    def load_lab_reports(self) -> List[Document]:
        try:
            self.logger.log_system("info", "Initializing loading data from load_lab_reports")
            docs = self.load_documents_from_dir("docs/lab_reports", ['.txt', '.pdf', '.xlsx', '.csv'])
            if docs:
                self.logger.log_system("info", f"Successfully loaded {len(docs)} lab reports")
            else:
                self.logger.log_system("warning", "No lab reports found in the directory.")
            return docs
        except Exception as e:
            self.logger.log_system("error", f"Failed to load lab reports: {e}")
            return []


    def load_prescriptions(self) -> List[Document]:
        try:
            self.logger.log_system("info", "Initializing loading data from load_prescriptions")
            docs = self.load_documents_from_dir("docs/prescriptions", ['.txt', '.pdf', '.xlsx'])
            if docs:
                self.logger.log_system("info", f"Successfully loaded {len(docs)} prescriptions")
            else:
                self.logger.log_system("warning", "No prescription reports found in the directory.")
            return docs
        except Exception as e:
            self.logger.log_system("error", f"Failed to load prescriptions: {e}")
            return []

def main():
    ingest = Ingestion()
    lab_reports = ingest.load_lab_reports()
    prescriptions = ingest.load_prescriptions()
    print("Lab Reports:", lab_reports)
    print("Prescriptions:", prescriptions)

if __name__ == '__main__':
    main()
