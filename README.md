# AI Multi-Document Summarizer

A Streamlit application that combines several documents into a structured AI-generated summary. It also extracts candidate facts, identifies possible contradictions, displays heuristic reliability scores, and provides advanced features like entity extraction and semantic similarity analysis.

## 🚀 Live Demo

**[Access the deployed app here](https://madhubalan098-multi-doc-summarizer.streamlit.app)** *(Update this link with your actual deployment URL)*

## ✨ Key Features

### Core Capabilities
- **Multi-Document Summarization:** Upload multiple `.txt`, `.pdf`, and `.docx` documents for unified analysis
- **Contradiction Detection:** Automatically identifies conflicting information across sources using NLI models
- **Source Reliability Scoring:** Heuristic-based trustworthiness assessment for each document
- **Named Entity Extraction:** Automatically extracts people, organizations, and locations with frequency tracking
- **Semantic Similarity Analysis:** Visualizes how related extracted facts are to each other

### Advanced Features
- **Customizable Processing:**
  - Adjustable chunk size (200-600 words)
  - Summary detail levels (Short / Medium / Detailed)
  - Toggle entity extraction and visualizations
- **Interactive Visualizations:**
  - Reliability bar charts
  - Document size distribution
  - Semantic similarity heatmap
  - Entity frequency charts
  - Document comparison view
- **Export Functionality:**
  - JSON export with complete structured data
  - Text report export for easy sharing
  - Timestamped filenames

### User Experience
- Tab-based navigation for organized results
- Real-time progress tracking
- Expandable sections for detailed analysis
- Side-by-side document comparison
- Mobile-friendly responsive design

## Requirements

- Python 3.10 or later
- Internet access on the first run to download the Hugging Face models and the spaCy language model
- Sufficient RAM and disk space for the ML models; `flan-t5-large` is particularly resource-intensive

## Setup

1. Open a terminal in this directory:

   ```powershell
   cd multi_doc_summarizer
   ```

2. Create and activate a virtual environment (recommended):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

## Run the app

Start the Streamlit interface directly:

```powershell
streamlit run app.py
```

Or use the included launcher:

```powershell
python main.py
```

Streamlit will print a local URL (normally `http://localhost:8501`) to open in a browser.

## How to use it

1. Upload one or more TXT, PDF, or DOCX files.
2. Select **Generate Summary**.
3. Wait while the models load and the documents are processed.
4. Review the generated summary, possible contradictions, source scores, and chart.

## How reliability scores work

Reliability is currently a filename-based demonstration heuristic, not a measure of factual accuracy. The app assigns scores based on terms in each filename:

| Filename pattern | Score |
| --- | ---: |
| Contains `research` or `paper`, or ends in `.pdf` | 0.95 |
| Contains `wiki` | 0.85 |
| Contains `news` | 0.75 |
| Contains `blog` | 0.50 |
| Any other filename | 0.70 |

## Technology Stack

### AI Models
- **DistilBART-CNN-12-6:** Efficient document chunk summarization (~400MB)
- **FLAN-T5-base:** Instruction-following unified summary generation (~900MB)
- **DeBERTa-v3-base:** Advanced NLI for contradiction detection (~500MB)
- **BERT-base-NER:** Named entity recognition for people, organizations, locations
- **all-MiniLM-L6-v2:** Sentence embeddings for semantic similarity analysis

### Libraries & Tools
- **Streamlit:** Interactive web application framework
- **Transformers (Hugging Face):** Pre-trained NLP models
- **NLTK:** Sentence tokenization
- **Plotly & Seaborn:** Interactive visualizations
- **scikit-learn:** Cosine similarity calculations
- **PyPDF, python-docx:** Document parsing

## Project structure

```text
multi_doc_summarizer/
|-- app.py                         # Streamlit user interface and processing workflow
|-- main.py                        # Simple Streamlit launcher
|-- requirements.txt               # Python dependencies
|-- data/sample_docs/              # Place for sample documents
`-- models/
    |-- summarizer.py              # BART and FLAN-T5 summarization
    |-- fact_extractor.py          # spaCy sentence extraction
    |-- contradiction_detector.py  # RoBERTa MNLI comparison
    `-- reliability_scoring.py     # Filename-based scoring heuristic
```

## Notes and limitations

- The app compares at most the first 30 extracted facts to limit the number of pairwise contradiction checks.
- Uploaded PDF text quality depends on the PDF containing extractable text; scanned PDFs may need OCR before upload.
- Contradiction results are model predictions and should be reviewed by a person.
- The first run can take a while because the required models are downloaded and loaded locally.
- **Deployment Note:** This app uses large ML models (BART, FLAN-T5-large, RoBERTa) that require significant memory (~4-6GB RAM). On Streamlit Community Cloud's free tier (1GB RAM), the app may experience memory issues with multiple users or large documents.

## Deployment

This app is deployed on Streamlit Community Cloud. To deploy your own instance:

1. Fork or clone this repository to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository, branch (main), and main file path (`app.py`)
6. Click "Deploy"

The deployment files are already configured:
- `requirements.txt` - Python dependencies with pinned versions
- `packages.txt` - System dependencies
- `.streamlit/config.toml` - Streamlit configuration
