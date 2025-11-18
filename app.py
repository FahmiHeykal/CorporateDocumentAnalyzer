import streamlit as st
import sys
import logging
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from modules.pdf_extractor import PDFExtractor
from modules.docx_extractor import DOCXExtractor
from modules.nlp_pipeline import NLPPipeline
from modules.summarizer import Summarizer
from modules.keyword_extractor import KeywordExtractor
from modules.sentiment_analyzer import SentimentAnalyzer
from modules.risk_detector import RiskDetector
from modules.export_pdf import PDFExporter
from modules.export_word import WordExporter
from utils.file_utils import FileUtils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CorporateDocumentAnalyzer:
    def __init__(self):
        self.file_utils = FileUtils()
        self.nlp_pipeline = NLPPipeline()
        self.summarizer = Summarizer()
        self.keyword_extractor = KeywordExtractor()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.risk_detector = RiskDetector()
        
    def setup_ui(self):
        st.set_page_config(page_title="Corporate Document Analyzer", page_icon="📊", layout="wide")
        st.title("📊 Corporate Document Analyzer")
        st.markdown("Analyze corporate documents for insights, risks, and opportunities")
        
    def sidebar_controls(self):
        st.sidebar.header("Document Upload")
        uploaded_file = st.sidebar.file_uploader("Choose a PDF or Word document", type=['pdf', 'docx'], help="Upload PDF or Word documents up to 200MB")
        analysis_mode = st.sidebar.selectbox("Analysis Mode", ["Summary", "Key Points", "Risk Analysis", "Opportunities", "Sentiment", "Full Report"])
        export_format = st.sidebar.selectbox("Export Format", ["PDF", "Word"])
        export_btn = st.sidebar.button("Export Results")
        return uploaded_file, analysis_mode, export_format, export_btn
    
    def extract_text(self, file_path, file_type):
        try:
            if file_type == "pdf":
                extractor = PDFExtractor()
                text = extractor.extract_text(file_path)
            elif file_type == "docx":
                extractor = DOCXExtractor()
                text = extractor.extract_text(file_path)
            else:
                return None
            return text if text and text.strip() else None
        except Exception as e:
            logger.error(f"Text extraction failed: {str(e)}")
            return None
    
    def analyze_document(self, text, mode):
        results = {}
        if mode in ["Summary", "Full Report"]:
            results['summary'] = self.summarizer.summarize(text)
        if mode in ["Key Points", "Full Report"]:
            results['keywords'] = self.keyword_extractor.extract_keywords(text)
            results['action_items'] = self.keyword_extractor.extract_action_items(text)
            results['decisions'] = self.keyword_extractor.extract_decisions(text)
        if mode in ["Risk Analysis", "Full Report"]:
            results['risks'] = self.risk_detector.detect_risks(text)
            results['opportunities'] = self.risk_detector.detect_opportunities(text)
        if mode in ["Sentiment", "Full Report"]:
            results['sentiment'] = self.sentiment_analyzer.analyze_sentiment(text)
        if mode == "Full Report":
            results['statistics'] = self.nlp_pipeline.get_statistics(text)
        return results
    
    def display_results(self, results, mode, original_text):
        if mode == "Summary":
            self.display_summary(results)
        elif mode == "Key Points":
            self.display_key_points(results)
        elif mode == "Risk Analysis":
            self.display_risk_analysis(results)
        elif mode == "Opportunities":
            self.display_opportunities(results)
        elif mode == "Sentiment":
            self.display_sentiment(results)
        elif mode == "Full Report":
            self.display_full_report(results, original_text)
    
    def display_summary(self, results):
        st.header("Executive Summary")
        st.write(results.get('summary', 'No summary available'))
    
    def display_key_points(self, results):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("🔑 Keywords")
            for keyword in results.get('keywords', [])[:10]:
                st.write(f"- {keyword}")
        with col2:
            st.subheader("✅ Action Items")
            for action in results.get('action_items', [])[:10]:
                st.write(f"- {action}")
        with col3:
            st.subheader("📋 Decisions")
            for decision in results.get('decisions', [])[:10]:
                st.write(f"- {decision}")
    
    def display_risk_analysis(self, results):
        st.header("🔴 Risk Analysis")
        for risk in results.get('risks', [])[:15]:
            st.write(f"- {risk}")
    
    def display_opportunities(self, results):
        st.header("🟢 Opportunities")
        for opportunity in results.get('opportunities', [])[:15]:
            st.write(f"- {opportunity}")
    
    def display_sentiment(self, results):
        st.header("😊 Sentiment Analysis")
        sentiment = results.get('sentiment', {})
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Overall Score", f"{sentiment.get('score', 0):.2f}")
        with col2:
            st.metric("Sentiment", sentiment.get('label', 'Neutral'))
        with col3:
            st.metric("Confidence", f"{sentiment.get('confidence', 0):.2f}")
    
    def display_full_report(self, results, original_text):
        st.header("📊 Full Analysis Report")
        tabs = st.tabs(["Summary", "Key Insights", "Risks & Opportunities", "Statistics", "Document Preview"])
        with tabs[0]:
            st.subheader("Executive Summary")
            st.write(results.get('summary', 'No summary available'))
        with tabs[1]:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("✅ Action Items")
                for action in results.get('action_items', []):
                    st.write(f"- {action}")
            with col2:
                st.subheader("📋 Decisions")
                for decision in results.get('decisions', []):
                    st.write(f"- {decision}")
                st.subheader("🔑 Keywords")
                for keyword in results.get('keywords', [])[:15]:
                    st.write(f"- {keyword}")
        with tabs[2]:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🔴 Risks")
                for risk in results.get('risks', []):
                    st.write(f"- {risk}")
            with col2:
                st.subheader("🟢 Opportunities")
                for opportunity in results.get('opportunities', []):
                    st.write(f"- {opportunity}")
        with tabs[3]:
            st.subheader("Document Statistics")
            stats = results.get('statistics', {})
            col1, col2, col3, col4 = st.columns(4)
            st.metric("Words", stats.get('word_count', 0))
            st.metric("Sentences", stats.get('sentence_count', 0))
            st.metric("Paragraphs", stats.get('paragraph_count', 0))
            st.metric("Reading Time", f"{stats.get('reading_time_minutes', 0)} min")
        with tabs[4]:
            preview_text = original_text[:5000] + "..." if len(original_text) > 5000 else original_text
            st.subheader("Document Preview")
            st.text_area("Extracted Text", preview_text, height=300)
    
    def run(self):
        self.setup_ui()
        uploaded_file, analysis_mode, export_format, export_btn = self.sidebar_controls()
        if uploaded_file:
            file_path = self.file_utils.save_uploaded_file(uploaded_file)
            file_type = uploaded_file.type.split('/')[-1]
            extracted_text = self.extract_text(file_path, file_type)
            if extracted_text:
                results = self.analyze_document(extracted_text, analysis_mode)
                self.display_results(results, analysis_mode, extracted_text)
                if export_btn:
                    if export_format == "PDF":
                        exporter = PDFExporter()
                    else:
                        exporter = WordExporter()
                    export_file = exporter.export(results, analysis_mode)
                    st.download_button(label=f"Download {export_format} Report", data=export_file, file_name=f"document_analysis_report.{export_format.lower()}", mime=f"application/{export_format.lower()}")
            else:
                st.error("Failed to extract text from the document.")
        else:
            st.info("Please upload a PDF or Word document to begin analysis.")

if __name__ == "__main__":
    analyzer = CorporateDocumentAnalyzer()
    analyzer.run()
