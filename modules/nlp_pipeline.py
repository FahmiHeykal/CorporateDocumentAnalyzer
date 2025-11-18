import spacy
import re
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class NLPPipeline:
    def __init__(self):
        self.nlp = None
        self._initialize_nlp()
    
    def _initialize_nlp(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy NLP pipeline initialized successfully")
        except OSError:
            logger.warning("spaCy model not found, using simple text processing")
            self.nlp = None
    
    def get_statistics(self, text: str) -> Dict[str, Any]:
        if not text.strip():
            return self._get_empty_statistics()
        return self._get_statistics_with_spacy(text) if self.nlp else self._get_statistics_simple(text)
    
    def _get_statistics_with_spacy(self, text: str) -> Dict[str, Any]:
        doc = self.nlp(text)
        sentences = list(doc.sents)
        paragraphs = [p for p in text.split('\n\n') if p.strip()]
        word_count = len([token for token in doc if not token.is_punct and not token.is_space])
        sentence_count = len(sentences)
        paragraph_count = len(paragraphs)
        reading_time_minutes = word_count / 200
        entities = {}
        for ent in doc.ents:
            if ent.label_ not in entities:
                entities[ent.label_] = []
            if ent.text not in entities[ent.label_]:
                entities[ent.label_].append(ent.text)
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'paragraph_count': paragraph_count,
            'reading_time_minutes': round(reading_time_minutes, 1),
            'entities': entities,
            'avg_sentence_length': round(word_count / sentence_count, 2) if sentence_count > 0 else 0
        }
    
    def _get_statistics_simple(self, text: str) -> Dict[str, Any]:
        words = re.findall(r'\b\w+\b', text)
        sentences = re.split(r'[.!?]+', text)
        paragraphs = [p for p in text.split('\n\n') if p.strip()]
        word_count = len(words)
        sentence_count = len([s for s in sentences if s.strip()])
        paragraph_count = len(paragraphs)
        reading_time_minutes = word_count / 200
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'paragraph_count': paragraph_count,
            'reading_time_minutes': round(reading_time_minutes, 1),
            'entities': {},
            'avg_sentence_length': round(word_count / sentence_count, 2) if sentence_count > 0 else 0
        }
    
    def _get_empty_statistics(self) -> Dict[str, Any]:
        return {'word_count': 0, 'sentence_count': 0, 'paragraph_count': 0, 'reading_time_minutes': 0, 'entities': {}, 'avg_sentence_length': 0}
    
    def preprocess_text(self, text: str) -> str:
        if not self.nlp:
            return self._simple_preprocess(text)
        doc = self.nlp(text)
        cleaned_tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
        return " ".join(cleaned_tokens)
    
    def _simple_preprocess(self, text: str) -> str:
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'any', 'can', 'her', 'was', 'one', 'our', 'out', 'who', 'get', 'has', 'had', 'him'}
        filtered_words = [word for word in words if word not in stop_words]
        return " ".join(filtered_words)
    
    def extract_entities(self, text: str) -> Dict[str, list]:
        if not self.nlp:
            return {}
        doc = self.nlp(text)
        entities = {}
        for ent in doc.ents:
            if ent.label_ not in entities:
                entities[ent.label_] = []
            if ent.text not in entities[ent.label_]:
                entities[ent.label_].append(ent.text)
        return entities
    
    def segment_sentences(self, text: str) -> list:
        if self.nlp:
            doc = self.nlp(text)
            return [sent.text.strip() for sent in doc.sents]
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
