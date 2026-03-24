import streamlit as st
import os
import tempfile
from preprocessing import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt, split_text_into_chunks
from embeddings import VectorStore
from summarizer import SummarizerModule
from contradiction_checker import ContradictionChecker
from conflict_resolver import ConflictResolver
from final_summary import FinalSummaryGenerator

# Page Config
st.set_page_config(page_title="Multi-Document Summarizer", page_icon="📝", layout="wide")

st.title("📝  Real-Time Multi-Document Summarizer")
st.markdown("Upload multiple documents to generate a unified summary, detect cross-document contradictions, and resolve conflicts dynamically.")

# --- Session State Management ---
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = VectorStore()
if 'summarizer' not in st.session_state:
    with st.spinner("Initializing Summarization Engine (this may take a moment on first load)..."):
        st.session_state.summarizer_module = SummarizerModule()
if 'checker' not in st.session_state:
    with st.spinner("Initializing Contradiction NLI Engine..."):
        st.session_state.checker = ContradictionChecker()

# --- Sidebar for Uploads ---
with st.sidebar:
    st.header("Upload Sources")
    uploaded_files = st.file_uploader("Upload PDF, DOCX, or TXT files", type=['pdf', 'docx', 'txt'], accept_multiple_files=True)
    
    process_button = st.button("Process Documents")

# --- Processing Logic ---
if process_button and uploaded_files:
    documents = []
    
    with st.spinner("Extracting text from documents..."):
        for uploaded_file in uploaded_files:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            # Save uploaded file temporarily to process it
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            # Extract Text
            text = ""
            if file_extension == 'pdf':
                text = extract_text_from_pdf(tmp_path)
            elif file_extension == 'docx':
                text = extract_text_from_docx(tmp_path)
            elif file_extension == 'txt':
                text = extract_text_from_txt(tmp_path)

            os.remove(tmp_path)
            if text:
                documents.append({"source": uploaded_file.name, "text": text})

    if not documents:
        st.error("No valid text could be extracted from the uploaded files.")
    else:
        # Show extraction stats
        st.success(f"Successfully processed {len(documents)} documents.")
        
        # 1. Chunking
        with st.spinner("Chunking texts..."):
            chunks = split_text_into_chunks(documents)
            st.info(f"Split documents into {len(chunks)} contextual chunks.")
            
        # 2. Embeddings
        with st.spinner("Building vector embeddings for semantic search..."):
            st.session_state.vector_store.build_index(chunks)
            
        col1, col2 = st.columns(2)
        
        # 3. Summarization
        with col1:
            st.subheader("1️⃣ Base Summary")
            with st.spinner("Generating base summary..."):
                base_summary = st.session_state.summarizer_module.summarize_chunks(chunks)
                st.write(base_summary)

        # 4. Contradiction Checking
        with col2:
            st.subheader("2️⃣ Contradiction Analysis")
            with st.spinner("Analyzing text chunks for contradictions..."):
                conflicts = st.session_state.checker.detect_conflicts_in_chunks(chunks)
                
            if conflicts:
                st.warning(f"Detected {len(conflicts)} potential contradictions between sources.")
                for c in conflicts:
                    with st.expander(f"Conflict: {c['docA']} vs {c['docB']}"):
                        st.markdown(f"**{c['docA']} says:**\n> {c['statementA']}")
                        st.markdown(f"**{c['docB']} says:**\n> {c['statementB']}")
            else:
                st.success("No apparent contradictions detected among the documents.")

        # 5. Resolution & Final Output
        st.divider()
        st.subheader("3️⃣ Final Resolved Synthesis")
        with st.spinner("Resolving conflicts and generating final output..."):
            resolver = ConflictResolver()
            resolutions = resolver.resolve(conflicts)
            
            final_gen = FinalSummaryGenerator(st.session_state.summarizer_module)
            final_output = final_gen.generate(base_summary, conflicts, resolutions)
            
            # Prettify the final output block
            st.markdown(f"""
            <div style="padding: 20px; border-radius: 10px; background-color: #1E1E1E; border: 1px solid #444;">
                <h4 style="color: #61DAFB;">Unified Output</h4>
                <p style="white-space: pre-wrap;">{final_output}</p>
            </div>
            """, unsafe_allow_html=True)
            
elif process_button and not uploaded_files:
    st.warning("Please upload at least one document from the sidebar to begin.")
