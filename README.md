# Corporate Document Analyzer

A Python-based Streamlit application for analyzing corporate documents using natural language processing (NLP).

## Features
📄 Upload and analyze PDF/Word documents  
🔤 Extract text and metadata offline  
📝 Generate executive summaries  
✅ Identify action items, risks, opportunities, and decisions  
😊 Sentiment analysis  
📊 Document statistics (word count, paragraphs, sentences, etc.)  
🔍 Keyword search with highlighting  
📥 Export results to PDF and Word  

## Tech Stack
**Frontend:** Streamlit  
**Backend:** Python 3.10+  
**NLP Libraries:** spaCy, Transformers  
**Document Processing:** PyMuPDF, python-docx, pdfplumber  
**Export:** ReportLab, python-docx  

## Installation
1. Clone the repository:  
`git clone https://github.com/username-kamu/CorporateDocumentAnalyzer.git`  
`cd CorporateDocumentAnalyzer`  

2. Install dependencies:  
`pip install -r requirements.txt`  

3. Download spaCy model:  
`python -m spacy download en_core_web_sm`  

4. Run the application:  
`streamlit run app.py`  

## Usage
1. Upload a PDF or Word document through the sidebar  
2. Select analysis mode (Summary, Key Points, Risk Analysis, etc.)  
3. View results in the main panel  
4. Export results to PDF or Word format  

## Project Structure
`CorporateDocumentAnalyzer/`  
`app.py - Main Streamlit application`  
`requirements.txt - Python dependencies`  
`README.md - Project documentation`  
`modules/ - Core analysis modules`  
`utils/ - Utility functions`  
`tests/ - Unit tests`  
`assets/ - Sample files and images`  
`models/ - Local model storage`  

## License
MIT License  

## Update Instructions
After making changes, push updates with:  
`git add .`  
`git commit -m "Update: describe your changes"`  
`git push origin main`
