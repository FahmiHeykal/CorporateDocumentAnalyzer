import re
from typing import List, Dict

class HighlightUtils:
    def __init__(self):
        self.highlight_colors = {
            'risk': '#ffcccc',
            'action_item': '#ffffcc',
            'decision': '#ccffcc',
            'opportunity': '#ccffff',
            'keyword': '#ffccff'
        }
    
    def highlight_text(self, text: str, patterns: Dict[str, List[str]]) -> str:
        highlighted_text = text
        
        for category, terms in patterns.items():
            color = self.highlight_colors.get(category, '#ffffff')
            for term in terms:
                pattern = re.compile(re.escape(term), re.IGNORECASE)
                highlighted_text = pattern.sub(
                    f'<span style="background-color: {color}; padding: 2px; border-radius: 2px;">{term}</span>',
                    highlighted_text
                )
        
        return highlighted_text
    
    def extract_highlight_patterns(self, results: Dict) -> Dict[str, List[str]]:
        patterns = {}
        
        if 'risks' in results:
            patterns['risk'] = self._extract_key_phrases(results['risks'])
        
        if 'action_items' in results:
            patterns['action_item'] = self._extract_key_phrases(results['action_items'])
        
        if 'decisions' in results:
            patterns['decision'] = self._extract_key_phrases(results['decisions'])
        
        if 'opportunities' in results:
            patterns['opportunity'] = self._extract_key_phrases(results['opportunities'])
        
        if 'keywords' in results:
            patterns['keyword'] = results['keywords'][:10]
        
        return patterns
    
    def _extract_key_phrases(self, items: List[str]) -> List[str]:
        phrases = []
        for item in items[:5]:
            words = item.split()[:5]
            phrases.append(' '.join(words))
        return phrases