import streamlit as st
import pandas as pd
import plotly.express as px
import networkx as nx
import plotly.graph_objects as go
import re
import json
from io import BytesIO
from pypdf import PdfReader
from docx import Document
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Initialize session state for lazy loading models
if 'summarizer' not in st.session_state:
    st.session_state.summarizer = None
if 'fact_extractor' not in st.session_state:
    st.session_state.fact_extractor = None
if 'contradiction_detector' not in st.session_state:
    st.session_state.contradiction_detector = None
if 'reliability_scorer' not in st.session_state:
    st.session_state.reliability_scorer = None
if 'entity_extractor' not in st.session_state:
    st.session_state.entity_extractor = None
if 'similarity_model' not in st.session_state:
    st.session_state.similarity_model = None

# We can lazy load the models within functions
def load_models():
    with st.spinner("Loading models... This may take a few minutes."):
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
        
        if st.session_state.entity_extractor is None:
            from models.entity_extractor import EntityExtractor
            st.session_state.entity_extractor = EntityExtractor()
        
        if st.session_state.similarity_model is None:
            st.session_state.similarity_model = SentenceTransformer('all-MiniLM-L6-v2')

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

def create_similarity_heatmap(facts, model):
    """Create semantic similarity heatmap for facts"""
    if len(facts) < 2:
        return None
    
    # Limit to top 10 facts for visualization
    top_facts = facts[:10]
    
    # Get embeddings
    embeddings = model.encode(top_facts)
    
    # Calculate similarity matrix
    similarity_matrix = cosine_similarity(embeddings)
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(similarity_matrix, annot=True, fmt='.2f', cmap='YlOrRd', 
                xticklabels=[f"Fact {i+1}" for i in range(len(top_facts))],
                yticklabels=[f"Fact {i+1}" for i in range(len(top_facts))],
                ax=ax, cbar_kws={'label': 'Similarity Score'})
    ax.set_title('Semantic Similarity Between Facts')
    plt.tight_layout()
    return fig

st.set_page_config(page_title="AI Multi-Document Summarizer", page_icon="📚", layout="wide")

st.title("📚 AI Multi-Document Summarizer")
st.markdown("**Analyze multiple documents with AI-powered summarization, contradiction detection, and entity extraction**")

# Sidebar for configuration
st.sidebar.header("⚙️ Configuration")
st.sidebar.markdown("---")

# Chunk size control
chunk_size = st.sidebar.slider(
    "Chunk Size (words)",
    min_value=200,
    max_value=600,
    value=350,
    step=50,
    help="Smaller chunks = more detailed processing but slower. Larger chunks = faster but less granular."
)

# Summary length control
summary_length = st.sidebar.select_slider(
    "Summary Detail Level",
    options=["Short", "Medium", "Detailed"],
    value="Medium",
    help="Short: Brief overview | Medium: Balanced | Detailed: Comprehensive summary"
)

# Map summary length to parameters
length_params = {
    "Short": {"max_length": 80, "min_length": 20},
    "Medium": {"max_length": 130, "min_length": 30},
    "Detailed": {"max_length": 200, "min_length": 50}
}

# Feature toggles
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Features")
enable_entities = st.sidebar.checkbox("Extract Named Entities", value=True, help="Extract people, organizations, locations")
enable_similarity = st.sidebar.checkbox("Show Similarity Heatmap", value=True, help="Visualize semantic similarity between facts")
enable_comparison = st.sidebar.checkbox("Document Comparison View", value=False, help="Side-by-side document comparison")

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Upload 2-5 documents for best results. Supports PDF, DOCX, and TXT formats.")

st.header("📤 Section 1: Upload Documents")
uploaded_files = st.file_uploader(
    "Upload multiple documents (TXT, PDF, DOCX)", 
    type=['txt', 'pdf', 'docx'], 
    accept_multiple_files=True,
    help="You can upload multiple files at once"
)

col1, col2 = st.columns([3, 1])
with col1:
    generate_btn = st.button("🚀 Generate Analysis", type="primary", use_container_width=True)
with col2:
    if st.session_state.get('results'):
        export_format = st.selectbox("Export", ["JSON", "Text Summary"], label_visibility="collapsed")

if generate_btn:
    if not uploaded_files:
        st.error("⚠️ Please upload at least one document.")
    else:
        load_models()
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Store all document texts for comparison
        doc_texts = []
        doc_summaries = []
        files_info = []
        
        # 1. Text Extraction & Preprocessing & Chunking
        for idx, file in enumerate(uploaded_files):
            status_text.text(f"📄 Processing {file.name}... ({idx+1}/{len(uploaded_files)})")
            progress_bar.progress((idx + 1) / (len(uploaded_files) + 6))
            
            raw_text = extract_text(file)
            clean_text = preprocess_text(raw_text)
            doc_texts.append(clean_text)
            chunks = chunk_text(clean_text, words_per_chunk=chunk_size)
            
            files_info.append({'name': file.name, 'size': len(clean_text.split()), 'chunks': len(chunks)})
            
            file_summaries = []
            params = length_params[summary_length]
            for i, chunk in enumerate(chunks):
                if len(chunk.split()) < 20: 
                    continue
                summ = st.session_state.summarizer.summarize_chunk(
                    chunk, 
                    max_length=params['max_length'], 
                    min_length=params['min_length']
                )
                file_summaries.append(summ)
            
            doc_summaries.append(" ".join(file_summaries))
        
        # 2. Extract Facts
        status_text.text("🔍 Extracting facts...")
        progress_bar.progress(0.5)
        all_facts = st.session_state.fact_extractor.extract_facts(doc_summaries)
        verified_facts = list(set(all_facts))
        
        # 3. Entity Extraction
        entities = None
        if enable_entities:
            status_text.text("👤 Extracting named entities...")
            progress_bar.progress(0.6)
            entities = st.session_state.entity_extractor.extract_entities(doc_texts)
        
        # 4. Contradiction Detection
        status_text.text("⚠️ Detecting contradictions...")
        progress_bar.progress(0.7)
        subset_facts = verified_facts[:30]
        contradictions = st.session_state.contradiction_detector.detect_contradictions(subset_facts)
        contradiction_texts = [f"Found contradiction: '{c['Statement 1']}' VS '{c['Statement 2']}'" for c in contradictions]
        
        # 5. Reliability Scoring
        status_text.text("📊 Calculating source reliability...")
        progress_bar.progress(0.8)
        reliability_scores = st.session_state.reliability_scorer.score_documents(files_info)
        
        # 6. Unified Summary Generation
        status_text.text("✍️ Generating final summary...")
        progress_bar.progress(0.9)
        final_summary = st.session_state.summarizer.generate_unified_summary(
            doc_summaries, 
            subset_facts, 
            contradiction_texts
        )
        
        progress_bar.progress(1.0)
        status_text.text("✅ Analysis complete!")
        
        # Store results in session state
        st.session_state.results = {
            'summary': final_summary,
            'facts': verified_facts,
            'contradictions': contradictions,
            'reliability': reliability_scores,
            'entities': entities,
            'files_info': files_info,
            'doc_summaries': doc_summaries,
            'doc_texts': doc_texts,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # --- UI DISPLAY ---
        st.success("🎉 Analysis completed successfully!")
        
        # Create tabs for better organization
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📝 Summary", 
            "⚠️ Contradictions", 
            "👥 Entities" if enable_entities else "📊 Reliability",
            "📊 Visualizations",
            "🔍 Document Comparison" if enable_comparison else "📁 Export"
        ])
        
        with tab1:
            st.header("📝 AI Generated Summary")
            st.markdown(f"**Generated:** {st.session_state.results['timestamp']}")
            st.markdown(f"**Detail Level:** {summary_length}")
            st.info(final_summary)
            
            # Show individual document summaries in expander
            with st.expander("📄 View Individual Document Summaries"):
                for i, (file, summary) in enumerate(zip(uploaded_files, doc_summaries)):
                    st.markdown(f"**{i+1}. {file.name}**")
                    st.write(summary)
                    st.markdown("---")
        
        with tab2:
            st.header("⚠️ Contradictions Detected")
            if contradictions:
                st.warning(f"Found {len(contradictions)} contradiction(s) across documents")
                df_contra = pd.DataFrame(contradictions)
                st.dataframe(df_contra, use_container_width=True)
                
                # Show details in expandable cards
                for i, contra in enumerate(contradictions):
                    with st.expander(f"Contradiction {i+1}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Statement 1:**")
                            st.info(contra['Statement 1'])
                        with col2:
                            st.markdown("**Statement 2:**")
                            st.info(contra['Statement 2'])
            else:
                st.success("✅ No contradictions detected among the key facts!")
        
        with tab3:
            if enable_entities and entities:
                st.header("👥 Named Entities Extracted")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if 'PERSON' in entities:
                        st.subheader("👤 People")
                        df_persons = pd.DataFrame(entities['PERSON'])
                        st.dataframe(df_persons, use_container_width=True)
                    
                    if 'LOC' in entities:
                        st.subheader("📍 Locations")
                        df_locs = pd.DataFrame(entities['LOC'])
                        st.dataframe(df_locs, use_container_width=True)
                
                with col2:
                    if 'ORG' in entities:
                        st.subheader("🏢 Organizations")
                        df_orgs = pd.DataFrame(entities['ORG'])
                        st.dataframe(df_orgs, use_container_width=True)
                    
                    if 'MISC' in entities:
                        st.subheader("🔖 Other Entities")
                        df_misc = pd.DataFrame(entities['MISC'])
                        st.dataframe(df_misc, use_container_width=True)
            else:
                st.header("📊 Source Reliability Scores")
                df_rels = pd.DataFrame(reliability_scores)
                st.dataframe(df_rels, use_container_width=True)
                
                st.subheader("Document Statistics")
                df_stats = pd.DataFrame(files_info)
                st.dataframe(df_stats, use_container_width=True)
        
        with tab4:
            st.header("📊 Visualizations")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Source Reliability")
                df_rels = pd.DataFrame(reliability_scores)
                fig_rel = px.bar(df_rels, x='Document', y='Reliability Score', 
                               title="Document Reliability Scores",
                               color='Reliability Score',
                               color_continuous_scale='Viridis')
                st.plotly_chart(fig_rel, use_container_width=True)
            
            with col2:
                st.subheader("Document Sizes")
                df_stats = pd.DataFrame(files_info)
                fig_size = px.pie(df_stats, values='size', names='name', 
                                title="Document Word Count Distribution")
                st.plotly_chart(fig_size, use_container_width=True)
            
            # Similarity Heatmap
            if enable_similarity and len(verified_facts) >= 2:
                st.subheader("🔥 Semantic Similarity Heatmap")
                st.caption("Shows how similar the extracted facts are to each other (top 10 facts)")
                fig_heatmap = create_similarity_heatmap(verified_facts, st.session_state.similarity_model)
                if fig_heatmap:
                    st.pyplot(fig_heatmap)
            
            # Entity visualization
            if enable_entities and entities:
                st.subheader("📊 Entity Frequency")
                all_entities_list = []
                for entity_type, entity_list in entities.items():
                    for item in entity_list[:5]:  # Top 5 per type
                        all_entities_list.append({
                            'Entity': item['entity'],
                            'Type': entity_type,
                            'Count': item['count']
                        })
                
                if all_entities_list:
                    df_entities = pd.DataFrame(all_entities_list)
                    fig_entities = px.bar(df_entities, x='Entity', y='Count', color='Type',
                                        title="Top Entities Across All Documents",
                                        barmode='group')
                    st.plotly_chart(fig_entities, use_container_width=True)
        
        with tab5:
            if enable_comparison:
                st.header("🔍 Document Comparison")
                if len(uploaded_files) >= 2:
                    col1, col2 = st.columns(2)
                    with col1:
                        doc1_idx = st.selectbox("Select Document 1", range(len(uploaded_files)), 
                                              format_func=lambda x: uploaded_files[x].name)
                    with col2:
                        doc2_idx = st.selectbox("Select Document 2", range(len(uploaded_files)), 
                                              format_func=lambda x: uploaded_files[x].name,
                                              index=min(1, len(uploaded_files)-1))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader(f"📄 {uploaded_files[doc1_idx].name}")
                        st.info(doc_summaries[doc1_idx])
                        st.caption(f"Word count: {files_info[doc1_idx]['size']}")
                    
                    with col2:
                        st.subheader(f"📄 {uploaded_files[doc2_idx].name}")
                        st.info(doc_summaries[doc2_idx])
                        st.caption(f"Word count: {files_info[doc2_idx]['size']}")
                else:
                    st.info("Upload at least 2 documents to enable comparison view.")
            else:
                st.header("📁 Export Results")
                
                # Prepare export data
                export_data = {
                    'analysis_date': st.session_state.results['timestamp'],
                    'configuration': {
                        'chunk_size': chunk_size,
                        'summary_length': summary_length
                    },
                    'documents': [f.name for f in uploaded_files],
                    'unified_summary': final_summary,
                    'facts': verified_facts[:20],
                    'contradictions': contradictions,
                    'reliability_scores': reliability_scores,
                    'entities': entities if enable_entities else None
                }
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # JSON export
                    json_str = json.dumps(export_data, indent=2)
                    st.download_button(
                        label="📥 Download JSON Report",
                        data=json_str,
                        file_name=f"summary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                with col2:
                    # Text export
                    text_report = f"""
AI MULTI-DOCUMENT SUMMARY REPORT
Generated: {st.session_state.results['timestamp']}
=====================================

DOCUMENTS ANALYZED:
{chr(10).join([f"- {f.name}" for f in uploaded_files])}

UNIFIED SUMMARY:
{final_summary}

CONTRADICTIONS DETECTED: {len(contradictions)}
{chr(10).join([f"- {c['Statement 1']} VS {c['Statement 2']}" for c in contradictions[:5]])}

KEY FACTS ({len(verified_facts)} total):
{chr(10).join([f"{i+1}. {fact}" for i, fact in enumerate(verified_facts[:10])])}
"""
                    st.download_button(
                        label="📥 Download Text Report",
                        data=text_report,
                        file_name=f"summary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
