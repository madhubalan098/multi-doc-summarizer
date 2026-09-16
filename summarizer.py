# Simplistic text summariser to act as proof of concept using pipelines from huggingface transformers.
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from transformers import pipeline

class SummarizerModule:
    def __init__(self):
        # We can use a lightweight open-source model like sshleifer/distilbart-cnn-12-6 or similar
        # Caution: First run will download the model weights (~1GB)
        print("Loading summarizing model...")
        self.summarizer = pipeline("summarization", model="t5-small")

    def summarize_chunks(self, chunks):
        if not chunks:
            return "No text available to summarize."
        
        # Combine text from chunks. Warning: For real usage, context window has to be managed.
        combined_text = " ".join([chunk['text'] for chunk in chunks])
        
        # Max input length for distilbart roughly 1024 tokens. 
        # We'll truncate it rudely for this simple example.
        text_to_summarize = combined_text[:3000] 

        # We set somewhat sane max_length based on input length
        max_length = min(150, max(20, len(text_to_summarize.split()) // 2))

        try:
            summary = self.summarizer(text_to_summarize, max_length=max_length, min_length=15, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            print(f"Summarizer error: {e}")
            return "Error while generating summary."

