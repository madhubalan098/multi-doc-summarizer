import torch
from transformers import pipeline, T5Tokenizer, T5ForConditionalGeneration

class Summarizer:
    def __init__(self):
        # Use smaller models for Streamlit Cloud deployment
        print("Loading individual summarizer (distilbart)...")
        # distilbart is lighter than bart-large-cnn
        self.indiv_summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=-1)
        
        print("Loading unified summarizer (FLAN-T5-base)...")
        # Use t5-base instead of t5-large to fit in Streamlit Cloud's 1GB RAM
        self.unified_model_name = "google/flan-t5-base"
        self.unified_tokenizer = T5Tokenizer.from_pretrained(self.unified_model_name)
        self.unified_model = T5ForConditionalGeneration.from_pretrained(self.unified_model_name)

    def summarize_chunk(self, text, max_length=130, min_length=30):
        # Using distilBART for chunk summarization
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
