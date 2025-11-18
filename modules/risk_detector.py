import re
from typing import List
import logging

logger = logging.getLogger(__name__)

class RiskDetector:
    def __init__(self):
        self.risk_keywords = {
            'high': ['risk', 'threat', 'danger', 'vulnerability', 'exposure', 'uncertainty', 'volatility'],
            'medium': ['challenge', 'issue', 'concern', 'problem', 'difficulty', 'obstacle'],
            'low': ['consideration', 'factor', 'aspect', 'element']
        }
        
        self.opportunity_keywords = {
            'high': ['opportunity', 'advantage', 'benefit', 'potential', 'growth', 'expansion', 'innovation'],
            'medium': ['improvement', 'enhancement', 'development', 'progress', 'advancement'],
            'low': ['possibility', 'option', 'alternative', 'prospect']
        }
    
    def detect_risks(self, text: str) -> List[str]:
        risk_patterns = [
            r'(?:high|significant|major|serious)\s+(?:risk|threat|danger)[^.!?]*[.!?]',
            r'(?:potential|possible)\s+risk[^.!?]*[.!?]',
            r'(?:may|could|might)\s+(?:result in|lead to|cause)\s+[^.!?]*[.!?]',
            r'(?:challenge|issue|problem)\s+(?:with|in|regarding)[^.!?]*[.!?]',
            r'(?:failure to|inability to)[^.!?]*[.!?]',
            r'(?:compliance|regulatory|legal)\s+(?:issue|risk|concern)[^.!?]*[.!?]'
        ]
        
        risks = []
        for pattern in risk_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            risks.extend(matches)
        
        sentence_risks = self._extract_risk_sentences(text)
        risks.extend(sentence_risks)
        
        return list(set([risk.strip() for risk in risks if len(risk.strip()) > 15]))
    
    def detect_opportunities(self, text: str) -> List[str]:
        opportunity_patterns = [
            r'(?:opportunity|potential|possibility)\s+(?:for|to|in)[^.!?]*[.!?]',
            r'(?:can|could)\s+(?:lead to|result in|create)[^.!?]*[.!?]',
            r'(?:benefit|advantage)\s+(?:of|for|in)[^.!?]*[.!?]',
            r'(?:growth|expansion|improvement)\s+(?:in|of|for)[^.!?]*[.!?]',
            r'(?:competitive advantage|market opportunity)[^.!?]*[.!?]'
        ]
        
        opportunities = []
        for pattern in opportunity_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            opportunities.extend(matches)
        
        sentence_opportunities = self._extract_opportunity_sentences(text)
        opportunities.extend(sentence_opportunities)
        
        return list(set([opp.strip() for opp in opportunities if len(opp.strip()) > 15]))
    
    def _extract_risk_sentences(self, text: str) -> List[str]:
        sentences = re.split(r'[.!?]+', text)
        risk_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            risk_score = 0
            
            for level, keywords in self.risk_keywords.items():
                for keyword in keywords:
                    if keyword in sentence_lower:
                        if level == 'high':
                            risk_score += 3
                        elif level == 'medium':
                            risk_score += 2
                        else:
                            risk_score += 1
            
            if risk_score >= 2 and len(sentence.strip()) > 20:
                risk_sentences.append(sentence.strip())
        
        return risk_sentences
    
    def _extract_opportunity_sentences(self, text: str) -> List[str]:
        sentences = re.split(r'[.!?]+', text)
        opportunity_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            opportunity_score = 0
            
            for level, keywords in self.opportunity_keywords.items():
                for keyword in keywords:
                    if keyword in sentence_lower:
                        if level == 'high':
                            opportunity_score += 3
                        elif level == 'medium':
                            opportunity_score += 2
                        else:
                            opportunity_score += 1
            
            if opportunity_score >= 2 and len(sentence.strip()) > 20:
                opportunity_sentences.append(sentence.strip())
        
        return opportunity_sentences