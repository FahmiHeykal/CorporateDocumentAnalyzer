import json
import csv
import io
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class ExportUtils:
    def __init__(self):
        pass
    
    def to_json(self, results: Dict[str, Any]) -> str:
        try:
            return json.dumps(results, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"JSON export failed: {str(e)}")
            return "{}"
    
    def to_csv(self, results: Dict[str, Any]) -> str:
        try:
            output = io.StringIO()
            writer = csv.writer(output)
            
            if 'keywords' in results:
                writer.writerow(['Keywords'])
                for keyword in results['keywords']:
                    writer.writerow([keyword])
                writer.writerow([])
            
            if 'action_items' in results:
                writer.writerow(['Action Items'])
                for item in results['action_items']:
                    writer.writerow([item])
                writer.writerow([])
            
            if 'risks' in results:
                writer.writerow(['Risks'])
                for risk in results['risks']:
                    writer.writerow([risk])
                writer.writerow([])
            
            return output.getvalue()
        except Exception as e:
            logger.error(f"CSV export failed: {str(e)}")
            return ""
    
    def format_for_export(self, results: Dict[str, Any]) -> Dict[str, Any]:
        formatted = {}
        
        for key, value in results.items():
            if isinstance(value, (str, int, float, bool)):
                formatted[key] = value
            elif isinstance(value, list):
                formatted[key] = [str(item) for item in value]
            elif isinstance(value, dict):
                formatted[key] = {k: str(v) for k, v in value.items()}
            else:
                formatted[key] = str(value)
        
        return formatted
