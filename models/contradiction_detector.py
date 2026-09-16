from transformers import pipeline

class ContradictionDetector:
    def __init__(self):
        print("Loading NLI model (roberta-large-mnli)...")
        # Initialize NLI pipeline with RoBERTa
        self.nli_pipeline = pipeline("text-classification", model="roberta-large-mnli")
    
    def detect_contradictions(self, facts):
        contradictions = []
        n_facts = len(facts)
        # Compare each fact with all other ones. This is O(n^2), so for demo we just do a simple pass
        for i in range(n_facts):
            for j in range(i+1, n_facts):
                fact_a = facts[i]
                fact_b = facts[j]
                # To check contradiction, we say fact_a is the premise and fact_b is the hypothesis.
                text_input = f"{fact_a} </s></s> {fact_b}"
                result = self.nli_pipeline(text_input, truncation=True)
                label = result[0]['label']
                if label == 'CONTRADICTION':
                    contradictions.append({
                        'Statement 1': fact_a,
                        'Statement 2': fact_b,
                        'Status': 'Contradiction'
                    })
        return contradictions
