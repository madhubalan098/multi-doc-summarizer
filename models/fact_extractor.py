import spacy

class FactExtractor:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            import os
            os.system('python -m spacy download en_core_web_sm')
            self.nlp = spacy.load("en_core_web_sm")

    def extract_facts(self, summaries):
        # Extracts statements (facts) from text summaries
        facts = []
        for summary in summaries:
            doc = self.nlp(summary)
            for sent in doc.sents:
                facts.append(sent.text.strip())
        return facts
