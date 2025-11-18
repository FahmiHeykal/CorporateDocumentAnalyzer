import re
from typing import List
import logging

logger = logging.getLogger(__name__)

class KeywordExtractor:
    def __init__(self):
        pass
    
    def extract_keywords(self, text: str, top_n: int = 20) -> List[str]:
        return self._simple_keyword_extraction(text, top_n)
    
    def extract_action_items(self, text: str) -> List[str]:
        action_patterns = [
            r'(?:need to|must|should|will)\s+([^.!?]*(?:implement|complete|finish|submit|review|approve|prepare|send|check|verify)[^.!?]*[.!?])',
            r'(?:action item|todo|task):?\s*([^.!?]*[.!?])',
            r'(?:please|kindly)\s+([^.!?]*(?:prepare|send|check|verify)[^.!?]*[.!?])',
            r'(?:ensure|make sure)\s+([^.!?]*[.!?])',
            r'(?:required to|expected to)\s+([^.!?]*[.!?])'
        ]
        
        actions = []
        for pattern in action_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            actions.extend(matches)
        
        return [action.strip() for action in actions if len(action.strip()) > 10]
    
    def extract_decisions(self, text: str) -> List[str]:
        decision_patterns = [
            r'(?:decided|agreed|concluded|resolved)\s+([^.!?]*[.!?])',
            r'(?:decision|resolution):?\s*([^.!?]*[.!?])',
            r'(?:it was|we have)\s+(?:decided|agreed)\s+([^.!?]*[.!?])',
            r'(?:the board|committee|team)\s+(?:approved|rejected)\s+([^.!?]*[.!?])',
            r'(?:conclusion|agreement)\s+([^.!?]*[.!?])'
        ]
        
        decisions = []
        for pattern in decision_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            decisions.extend(matches)
        
        return [decision.strip() for decision in decisions if len(decision.strip()) > 10]
    
    def _simple_keyword_extraction(self, text: str, top_n: int) -> List[str]:
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'any', 'can', 
            'her', 'was', 'one', 'our', 'out', 'who', 'get', 'has', 'had', 'him', 
            'how', 'man', 'its', 'now', 'old', 'see', 'two', 'way', 'boy', 
            'did', 'let', 'put', 'say', 'she', 'too', 'use', 'that', 'with',
            'this', 'from', 'have', 'they', 'which', 'their', 'what', 'when', 'where',
            'your', 'will', 'would', 'there', 'been', 'were', 'them', 'than', 'then'
        }
        
        filtered_words = [word for word in words if word not in stop_words]
        
        word_freq = {}
        for word in filtered_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:top_n]]
