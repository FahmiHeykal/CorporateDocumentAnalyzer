from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from typing import Dict
import io
import logging

logger = logging.getLogger(__name__)

class PDFExporter:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.custom_styles = self._create_custom_styles()
    
    def _create_custom_styles(self):
        custom_styles = {
            'Title': ParagraphStyle(
                'CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=16,
                spaceAfter=12,
                textColor=colors.darkblue
            ),
            'Heading2': ParagraphStyle(
                'CustomHeading2',
                parent=self.styles['Heading2'],
                fontSize=14,
                spaceAfter=6,
                textColor=colors.darkblue
            ),
            'Normal': ParagraphStyle(
                'CustomNormal',
                parent=self.styles['Normal'],
                fontSize=10,
                spaceAfter=6
            ),
            'Bullet': ParagraphStyle(
                'CustomBullet',
                parent=self.styles['Normal'],
                fontSize=10,
                leftIndent=10,
                spaceAfter=3
            )
        }
        return custom_styles
    
    def export(self, results: Dict, analysis_type: str) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        
        story.append(Paragraph("Corporate Document Analysis Report", self.custom_styles['Title']))
        story.append(Spacer(1, 12))
        
        if 'summary' in results:
            story.append(Paragraph("Executive Summary", self.custom_styles['Heading2']))
            story.append(Paragraph(results['summary'], self.custom_styles['Normal']))
            story.append(Spacer(1, 12))
        
        if 'action_items' in results and results['action_items']:
            story.append(Paragraph("Action Items", self.custom_styles['Heading2']))
            for item in results['action_items'][:10]:
                story.append(Paragraph(f"• {item}", self.custom_styles['Bullet']))
            story.append(Spacer(1, 12))
        
        if 'decisions' in results and results['decisions']:
            story.append(Paragraph("Decisions", self.custom_styles['Heading2']))
            for decision in results['decisions'][:10]:
                story.append(Paragraph(f"• {decision}", self.custom_styles['Bullet']))
            story.append(Spacer(1, 12))
        
        if 'risks' in results and results['risks']:
            story.append(Paragraph("Risks", self.custom_styles['Heading2']))
            for risk in results['risks'][:10]:
                story.append(Paragraph(f"• {risk}", self.custom_styles['Bullet']))
            story.append(Spacer(1, 12))
        
        if 'opportunities' in results and results['opportunities']:
            story.append(Paragraph("Opportunities", self.custom_styles['Heading2']))
            for opportunity in results['opportunities'][:10]:
                story.append(Paragraph(f"• {opportunity}", self.custom_styles['Bullet']))
            story.append(Spacer(1, 12))
        
        if 'keywords' in results and results['keywords']:
            story.append(Paragraph("Key Keywords", self.custom_styles['Heading2']))
            keywords_text = ", ".join(results['keywords'][:15])
            story.append(Paragraph(keywords_text, self.custom_styles['Normal']))
            story.append(Spacer(1, 12))
        
        if 'sentiment' in results:
            sentiment = results['sentiment']
            story.append(Paragraph("Sentiment Analysis", self.custom_styles['Heading2']))
            sentiment_text = f"Label: {sentiment.get('label', 'N/A')}, Score: {sentiment.get('score', 0):.2f}, Confidence: {sentiment.get('confidence', 0):.2f}"
            story.append(Paragraph(sentiment_text, self.custom_styles['Normal']))
            story.append(Spacer(1, 12))
        
        if 'statistics' in results:
            stats = results['statistics']
            story.append(Paragraph("Document Statistics", self.custom_styles['Heading2']))
            
            stats_data = [
                ["Metric", "Value"],
                ["Word Count", str(stats.get('word_count', 0))],
                ["Sentence Count", str(stats.get('sentence_count', 0))],
                ["Paragraph Count", str(stats.get('paragraph_count', 0))],
                ["Reading Time", f"{stats.get('reading_time_minutes', 0)} minutes"],
                ["Average Sentence Length", f"{stats.get('avg_sentence_length', 0):.2f} words"]
            ]
            
            stats_table = Table(stats_data, colWidths=[2*inch, 2*inch])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(stats_table)
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()