class ReliabilityScoring:
    def __init__(self):
        pass

    def get_score(self, filename):
        name_lower = filename.lower()
        if "research" in name_lower or "paper" in name_lower or name_lower.endswith(".pdf"):
            return 0.95
        elif "wiki" in name_lower:
            return 0.85
        elif "news" in name_lower:
            return 0.75
        elif "blog" in name_lower:
            return 0.50
        else:
            return 0.70 # Default

    def score_documents(self, file_params_list):
        scores = []
        for file in file_params_list:
            score = self.get_score(file['name'])
            scores.append({
                'Document': file['name'],
                'Reliability Score': score
            })
        return scores
