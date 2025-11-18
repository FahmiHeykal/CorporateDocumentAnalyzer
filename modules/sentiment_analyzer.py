from transformers import pipeline
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = None
        self._initialize_analyzer()
    
    def _initialize_analyzer(self):
        try:
            self.analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=-1
            )
            logger.info("Transformer sentiment analyzer initialized successfully")
        except Exception as e:
            logger.warning(f"Transformer sentiment analyzer failed: {str(e)}")
            logger.info("Using rule-based sentiment analysis as fallback")
            self.analyzer = None
    
    def analyze_sentiment(self, text: str) -> Dict:
        if not text.strip():
            return {'label': 'NEUTRAL', 'score': 0.5, 'confidence': 0.0}
        
        try:
            if self.analyzer and len(text) > 10:
                if len(text) > 512:
                    chunks = self._split_text(text, 500)
                    sentiments = [self.analyzer(chunk[:512])[0] for chunk in chunks if len(chunk) > 10]
                    if not sentiments:
                        return self._rule_based_sentiment(text)
                    
                    positive_count = sum(1 for s in sentiments if s['label'] == 'POSITIVE')
                    avg_score = sum(s['score'] for s in sentiments) / len(sentiments)
                    overall_label = 'POSITIVE' if positive_count > len(sentiments) / 2 else 'NEGATIVE'
                    
                    return {'label': overall_label, 'score': avg_score, 'confidence': avg_score}
                else:
                    result = self.analyzer(text[:512])[0]
                    return {'label': result['label'], 'score': result['score'], 'confidence': result['score']}
            else:
                return self._rule_based_sentiment(text)
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {str(e)}")
            return self._rule_based_sentiment(text)
    
    def _rule_based_sentiment(self, text: str) -> Dict:
        positive_words = {
            'good', 'great', 'excellent', 'positive', 'success', 'profit', 'growth', 
            'improve', 'benefit', 'opportunity', 'strong', 'better', 'best', 'win', 
            'advantage', 'achievement', 'progress', 'successful', 'outstanding'
        }
        negative_words = {
            'bad', 'poor', 'negative', 'loss', 'decline', 'risk', 'problem', 'issue', 
            'challenge', 'weak', 'worse', 'worst', 'fail', 'disadvantage', 'threat',
            'difficult', 'concern', 'weakness', 'failure'
        }
        
        words = text.lower().split()
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        total = positive_count + negative_count
        
        if total == 0:
            return {'label': 'NEUTRAL', 'score': 0.5, 'confidence': 0.0}
        
        score = positive_count / total
        confidence = abs(score - 0.5) * 2
        
        if score > 0.6:
            label = 'POSITIVE'
        elif score < 0.4:
            label = 'NEGATIVE'
        else:
            label = 'NEUTRAL'
        
        return {'label': label, 'score': score, 'confidence': confidence}
    
    def _split_text(self, text: str, chunk_size: int) -> list:
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
