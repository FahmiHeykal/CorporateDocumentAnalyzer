import unittest
from modules.docx_extractor import DOCXExtractor

class TestDOCXExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = DOCXExtractor()
    
    def test_extractor_initialization(self):
        self.assertIsNotNone(self.extractor)
    
    def test_extract_text_method_exists(self):
        self.assertTrue(hasattr(self.extractor, 'extract_text'))

if __name__ == '__main__':
    unittest.main()
