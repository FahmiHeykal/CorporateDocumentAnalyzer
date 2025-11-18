import unittest
from modules.pdf_extractor import PDFExtractor

class TestPDFExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = PDFExtractor()
    
    def test_extractor_initialization(self):
        self.assertIsNotNone(self.extractor)
        self.assertEqual(self.extractor.text_engine, "fitz")
    
    def test_extract_methods_exist(self):
        self.assertTrue(hasattr(self.extractor, 'extract_text'))
        self.assertTrue(hasattr(self.extractor, 'extract_metadata'))
        self.assertTrue(hasattr(self.extractor, 'extract_tables'))
        self.assertTrue(hasattr(self.extractor, 'extract_images'))

if __name__ == '__main__':
    unittest.main()
