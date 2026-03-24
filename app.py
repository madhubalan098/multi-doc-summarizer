import os
from preprocessing import load_documents, split_text_into_chunks
from embeddings import VectorStore
from summarizer import SummarizerModule
from contradiction_checker import ContradictionChecker
from conflict_resolver import ConflictResolver
from final_summary import FinalSummaryGenerator

def main():
    print("=== Multi-Doc Summarizer Started ===")
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    
    # Ensure data dir exists
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created data directory at {data_dir}. Please place documents (.txt, .pdf, .docx) there to run.")
        return

    # 1. Load Documents
    print("\n1. Loading documents...")
    docs = load_documents(data_dir)
    print(f"Loaded {len(docs)} documents.")

    if not docs:
        print("No documents found in data dir.")
        return

    # 2. Chunking
    print("\n2. Chunking text...")
    chunks = split_text_into_chunks(docs)
    print(f"Split raw text into {len(chunks)} chunks.")

    # 3. Embedding and Indexing
    print("\n3. Building Vector Store...")
    vector_store = VectorStore()
    vector_store.build_index(chunks)

    # 4. Summarization (Base)
    print("\n4. Generating Initial Summary...")
    summarizer = SummarizerModule()
    # Summarizing a query-relevant subset or all text. Here, all text to demonstrate.
    base_summary = summarizer.summarize_chunks(chunks)
    print("Base summary:", base_summary)

    # 5. Contradiction Checking
    print("\n5. Checking for contradictions...")
    checker = ContradictionChecker()
    conflicts = checker.detect_conflicts_in_chunks(chunks)
    print(f"Detected {len(conflicts)} potential contradictions.")

    # 6. Conflict Resolution
    print("\n6. Resolving Conflicts...")
    resolver = ConflictResolver()
    resolutions = resolver.resolve(conflicts)
    for res in resolutions:
        print("Resolution:", res)

    # 7. Final Output Generation
    print("\n7. Generating Final Output...")
    final_gen = FinalSummaryGenerator(summarizer)
    final_output = final_gen.generate(base_summary, conflicts, resolutions)
    
    print("\n#############################################")
    print(final_output)
    print("#############################################\n")

if __name__ == "__main__":
    main()
