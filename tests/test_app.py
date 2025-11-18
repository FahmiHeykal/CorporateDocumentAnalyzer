import unittest
from app import CorporateDocumentAnalyzer

class TestCorporateDocumentAnalyzer(unittest.TestCase):
    def test_app_initialization(self):
        analyzer = CorporateDocumentAnalyzer()
        
        self.assertIsNotNone(analyzer)
        self.assertIsNotNone(analyzer.file_utils)
        self.assertIsNotNone(analyzer.nlp_pipeline)

if __name__ == '__main__':
    unittest.main()
