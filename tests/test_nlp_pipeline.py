import unittest
from modules.nlp_pipeline import NLPPipeline

class TestNLPPipeline(unittest.TestCase):
    def setUp(self):
        self.nlp = NLPPipeline()
    
    def test_pipeline_initialization(self):
        self.assertIsNotNone(self.nlp)
        self.assertIsNotNone(self.nlp.nlp)
    
    def test_get_statistics(self):
        test_text = "This is a test sentence. This is another test sentence."
        stats = self.nlp.get_statistics(test_text)
        
        self.assertIn('word_count', stats)
        self.assertIn('sentence_count', stats)
        self.assertIn('paragraph_count', stats)
        self.assertIn('reading_time_minutes', stats)
        
        self.assertEqual(stats['word_count'], 10)
        self.assertEqual(stats['sentence_count'], 2)
    
    def test_preprocess_text(self):
        test_text = "This is a TEST document with some stop words."
        processed = self.nlp.preprocess_text(test_text)
        
        self.assertIsInstance(processed, str)
        self.assertNotIn('is', processed)
        self.assertIn('test', processed)
    
    def test_extract_entities(self):
        test_text = "Apple Inc. is located in Cupertino, California."
        entities = self.nlp.extract_entities(test_text)
        
        self.assertIsInstance(entities, dict)

if __name__ == '__main__':
    unittest.main()
