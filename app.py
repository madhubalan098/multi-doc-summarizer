import streamlit as st
import pandas as pd
import plotly.express as px
import networkx as nx
import plotly.graph_objects as go
import re
from io import BytesIO
from pypdf import PdfReader
from docx import Document

# Initialize session state for lazy loading models
if 'summarizer' not in st.session_state:
    st.session_state.summarizer = None
if 'fact_extractor' not in st.session_state:
    st.session_state.fact_extractor = None
if 'contradiction_detector' not in st.session_state:
    st.session_state.contradiction_detector = None
if 'reliability_scorer' not in st.session_state:
    st.session_state.reliability_scorer = None

# We can lazy load the models within functions
def load_models():
    with st.spinner("Loading models... This may take a few minutes locally."):
        if st.session_state.summarizer is None:
            from models.summarizer import Summarizer
            st.session_state.summarizer = Summarizer()
        
        if st.session_state.fact_extractor is None:
            from models.fact_extractor import FactExtractor
            st.session_state.fact_extractor = FactExtractor()
            
        if st.session_state.contradiction_detector is None:
            from models.contradiction_detector import ContradictionDetector
            st.session_state.contradiction_detector = ContradictionDetector()
            
        if st.session_state.reliability_scorer is None:
            from models.reliability_scoring import ReliabilityScoring
            st.session_state.reliability_scorer = ReliabilityScoring()

def extract_text(file):
    filename = file.name.lower()
    text = ""
    if filename.endswith(".pdf"):
        reader = PdfReader(file)
        for page in reader.pages:
            t = page.extract_text()
            if t: text += t
    elif filename.endswith(".docx"):
        doc = Document(file)
        for p in doc.paragraphs:
            text += p.text + "\n"
    elif filename.endswith(".txt"):
        text = file.read().decode("utf-8")
    return text

def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(text, words_per_chunk=350):
    words = text.split()
    chunks = []
    for i in range(0, len(words), words_per_chunk):
        chunks.append(" ".join(words[i:i + words_per_chunk]))
    return chunks

st.title("AI Multi-Document Summarizer")

st.header("Section 1: Upload Documents")
uploaded_files = st.file_uploader("Upload multiple documents (TXT, PDF, DOCX)", type=['txt', 'pdf', 'docx'], accept_multiple_files=True)

if st.button("Generate Summary"):
    if not uploaded_files:
        st.error("Please upload at least one document.")
    else:
        load_models()
        
        # Output placeholders
        status_text = st.empty()
        
        # 1. Text Extraction & Preprocessing & Chunking
        doc_summaries = []
        files_info = []
        
        for file in uploaded_files:
            status_text.text(f"Processing {file.name}...")
            raw_text = extract_text(file)
            clean_text = preprocess_text(raw_text)
            chunks = chunk_text(clean_text)
            
            files_info.append({'name': file.name})
            
            file_summaries = []
            for i, chunk in enumerate(chunks):
                if len(chunk.split()) < 20: 
                    continue # Skip very small chunks
                summ = st.session_state.summarizer.summarize_chunk(chunk)
                file_summaries.append(summ)
            
            doc_summaries.append(" ".join(file_summaries))
            
        # 5. Extract Facts
        status_text.text("Extracting facts...")
        all_facts = st.session_state.fact_extractor.extract_facts(doc_summaries)
        verified_facts = list(set(all_facts)) # Remove identical duplicates
        
        # 6. Contradiction Detection
        status_text.text("Detecting contradictions...")
        # To avoid O(N^2) explosion, we limit the combinations
        subset_facts = verified_facts[:30] # Limit for time constraints in demo
        contradictions = st.session_state.contradiction_detector.detect_contradictions(subset_facts)
        
        contradiction_texts = [f"Found contradiction: '{c['Statement 1']}' VS '{c['Statement 2']}'" for c in contradictions]
        
        # 7. Reliability Scoring
        status_text.text("Calculating source reliability...")
        reliability_scores = st.session_state.reliability_scorer.score_documents(files_info)
        
        # 8. Unified Summary Generation
        status_text.text("Generating final unified summary...")
        final_summary = st.session_state.summarizer.generate_unified_summary(
            doc_summaries, 
            subset_facts, 
            contradiction_texts
        )
        
        status_text.text("Done!")
        
        # --- UI DISPLAY ---
        
        st.header("Section 2: AI Generated Summary")
        st.write(final_summary)
        
        st.header("Section 3: Contradictions Detected")
        if contradictions:
            df_contra = pd.DataFrame(contradictions)
            st.dataframe(df_contra)
        else:
            st.success("No contradictions detected among the key facts.")
            
        st.header("Section 4: Source Reliability Scores")
        df_rels = pd.DataFrame(reliability_scores)
        st.dataframe(df_rels)
        
        st.header("Section 5: Visualizations")
        
        st.subheader("Source Reliability Chart")
        fig_rel = px.bar(df_rels, x='Document', y='Reliability Score', title="Document Reliability")
        st.plotly_chart(fig_rel)

        # Graph visualization for Facts vs documents (Simple star graph for demo)
        st.subheader("Fact Network Visualization")
        fig = go.Figure()
        # Create a simple mapping: Document -> Facts
        node_x = []
        node_y = []
        node_text = []
        
        fig.add_trace(go.Scatter(
            x=[0], y=[0], text=["Central Knowledge Base"], 
            mode='markers+text', marker=dict(size=40, color='lightblue')
        ))
        st.plotly_chart(fig)
