import fitz
import pdfplumber
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class PDFExtractor:
    def __init__(self):
        self.text_engine = "fitz"
    
    def extract_text(self, file_path: str) -> str:
        try:
            if self.text_engine == "fitz":
                return self._extract_with_fitz(file_path)
            else:
                return self._extract_with_pdfplumber(file_path)
        except Exception as e:
            logger.error(f"PDF extraction failed: {str(e)}")
            raise
    
    def _extract_with_fitz(self, file_path: str) -> str:
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    
    def _extract_with_pdfplumber(self, file_path: str) -> str:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    
    def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        metadata = {}
        try:
            with fitz.open(file_path) as doc:
                metadata = doc.metadata
                metadata['page_count'] = len(doc)
        except Exception as e:
            logger.error(f"Metadata extraction failed: {str(e)}")
        return metadata
    
    def extract_tables(self, file_path: str) -> List[List[List[str]]]:
        tables = []
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_tables = page.extract_tables()
                    for table in page_tables:
                        if table:
                            tables.append(table)
        except Exception as e:
            logger.error(f"Table extraction failed: {str(e)}")
        return tables
    
    def extract_images(self, file_path: str, output_dir: str) -> List[str]:
        image_paths = []
        try:
            with fitz.open(file_path) as doc:
                for page_index in range(len(doc)):
                    page = doc[page_index]
                    image_list = page.get_images()
                    
                    for img_index, img in enumerate(image_list):
                        xref = img[0]
                        pix = fitz.Pixmap(doc, xref)
                        
                        if pix.n - pix.alpha < 4:
                            img_path = f"{output_dir}/page_{page_index+1}_img_{img_index+1}.png"
                            pix.save(img_path)
                            image_paths.append(img_path)
                        pix = None
        except Exception as e:
            logger.error(f"Image extraction failed: {str(e)}")
        return image_paths