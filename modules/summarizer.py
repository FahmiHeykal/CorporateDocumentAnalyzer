from transformers import pipeline
from typing import List
import logging
import re

logger = logging.getLogger(__name__)

class Summarizer:
    def __init__(self):
        self.summarizer = None
        self._initialize_summarizer()
    
    def _initialize_summarizer(self):
        try:
            self.summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                tokenizer="facebook/bart-large-cnn",
                device=-1
            )
            logger.info("Transformer summarizer initialized successfully")
        except Exception as e:
            logger.warning(f"Transformer summarizer failed: {str(e)}")
            logger.info("Using extractive summarization as fallback")
            self.summarizer = None
    
    def summarize(self, text: str, max_length: int = 150, min_length: int = 30) -> str:
        if not text.strip():
            return "No text available for summarization."
        
        try:
            if self.summarizer and len(text) > 100:
                if len(text) > 1024:
                    chunks = self._split_text(text, 1000)
                    summaries = []
                    for chunk in chunks:
                        if len(chunk) > 50:
                            summary = self.summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
                            summaries.append(summary[0]['summary_text'])
                    return " ".join(summaries) if summaries else self._extractive_summarize(text)
                else:
                    summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
                    return summary[0]['summary_text']
            else:
                return self._extractive_summarize(text)
        except Exception as e:
            logger.error(f"Summarization failed: {str(e)}")
            return self._extractive_summarize(text)
    
    def _extractive_summarize(self, text: str, num_sentences: int = 3) -> str:
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= num_sentences:
            return ". ".join(sentences) + "."
        
        word_freq = {}
        for sentence in sentences:
            words = sentence.lower().split()
            for word in words:
                if len(word) > 2:
                    word_freq[word] = word_freq.get(word, 0) + 1
        
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            words = sentence.lower().split()
            if words:
                score = sum(word_freq.get(word, 0) for word in words if len(word) > 2) / len(words)
                sentence_scores[i] = score
        
        if not sentence_scores:
            return ". ".join(sentences[:num_sentences]) + "."
        
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
        top_sentences = sorted(top_sentences, key=lambda x: x[0])
        
        return ". ".join(sentences[i] for i, _ in top_sentences) + "."
    
    def _split_text(self, text: str, chunk_size: int) -> List[str]:
        sentences = text.split('.')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < chunk_size:
                current_chunk += sentence + "."
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence + "."
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
