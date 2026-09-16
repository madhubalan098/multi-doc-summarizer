from transformers import pipeline

class ContradictionChecker:
    def __init__(self, model_name="roberta-large-mnli"):
        print(f"Loading NLI model: {model_name}...")
        self.nli = pipeline("text-classification", model=model_name)

    def check_statements(self, statement_a, statement_b):
        '''
        Checks if statement B contradicts, entails or is neutral to statement A.
        '''
        # Transformers pipeline uses format: "statementA </s> statementB" 
        # or pair passing depending on model. For RoBERTa MNLI it's standard to pass pairs if supported.
        # But text-classification pipeline handles generic text. For NLI models you can usually pass pairs.
        pair = f"{statement_a} </s> {statement_b}"
        result = self.nli(pair)
        
        # RoBERTa-large-mnli returns: LABEL_0 (contradiction), LABEL_1 (neutral), LABEL_2 (entailment)
        # Using a safer way assuming human readable labels
        label = result[0]['label'].lower()
        
        if 'contradiction' in label or 'label_0' in label:
            return "Contradiction"
        elif 'entailment' in label or 'label_2' in label:
            return "Entailment"
        else:
            return "Neutral"

    def detect_conflicts_in_chunks(self, chunks):
        """
        Naive conflict detection: Compares every chunk against every other chunk (O(N^2)).
        In a real scenario, you would filter by semantic similarity first.
        """
        conflicts = []
        n = len(chunks)
        for i in range(n):
            for j in range(i + 1, n):
                res = self.check_statements(chunks[i]['text'], chunks[j]['text'])
                if res == "Contradiction":
                    conflicts.append({
                        "docA": chunks[i]['source'],
                        "statementA": chunks[i]['text'],
                        "docB": chunks[j]['source'],
                        "statementB": chunks[j]['text']
                    })
        return conflicts
