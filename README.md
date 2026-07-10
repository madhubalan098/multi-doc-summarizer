# AI Multi-Document Summarizer

A local Streamlit application that combines several documents into a structured AI-generated summary. It also extracts candidate facts, identifies possible contradictions, and displays heuristic reliability scores for each uploaded source.

## Features

- Upload multiple `.txt`, `.pdf`, and `.docx` documents.
- Extract and clean document text, then process it in manageable chunks.
- Create per-chunk summaries with `facebook/bart-large-cnn`.
- Produce a unified summary with `google/flan-t5-large`.
- Extract sentence-level candidate facts using spaCy.
- Detect potential contradictions with `roberta-large-mnli`.
- Display source-reliability scores and an interactive Plotly chart.

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
---

## 👨‍💻 Developed By
**Madhubalan**  
[GitHub Profile](https://github.com/madhubalan098) | multi-doc-summarizer

---
