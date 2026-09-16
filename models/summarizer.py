import torch
from transformers import pipeline, T5Tokenizer, T5ForConditionalGeneration

class Summarizer:
    def __init__(self):
        # We'll use a smaller model for faster local execution here, or just bart-large-cnn if specified.
        # But bart-large-cnn is heavy, let's stick to requirements.
        print("Loading individual summarizer (BART)...")
        self.indiv_summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
        print("Loading unified summarizer (FLAN-T5-large)...")
        # flan-t5-large is quite big (~3GB), using flan-t5-base to keep memory usage reasonable,
        # but the project asked for flan-t5-large. I will use google/flan-t5-large.
        self.unified_model_name = "google/flan-t5-large"
        self.unified_tokenizer = T5Tokenizer.from_pretrained(self.unified_model_name)
        self.unified_model = T5ForConditionalGeneration.from_pretrained(self.unified_model_name)

    def summarize_chunk(self, text, max_length=130, min_length=30):
        # Using BART for chunk summarization
        result = self.indiv_summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return result[0]['summary_text']

    def generate_unified_summary(self, summaries, verified_facts, contradictions):
        prompt = (
            "Read the following information from multiple sources and generate a detailed structured summary including: "
            "Overview, Key Points, Important Facts, Contradictions (if any), and Final Conclusion.\n\n"
        )
        prompt += "Input Summaries:\n" + "\n".join(summaries) + "\n\n"
        prompt += "Verified Facts:\n" + "\n".join(verified_facts) + "\n\n"
        prompt += "Contradictions:\n" + "\n".join(contradictions)

        inputs = self.unified_tokenizer(prompt, return_tensors="pt", max_length=1024, truncation=True)
        # the task asks for a single completion
        with torch.no_grad():
            outputs = self.unified_model.generate(
                inputs.input_ids,
                max_length=512,
                num_beams=4,
                early_stopping=True
            )
        return self.unified_tokenizer.decode(outputs[0], skip_special_tokens=True)
