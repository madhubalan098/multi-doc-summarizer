import nltk
from nltk.tokenize import sent_tokenize

class FactExtractor:
    def __init__(self):
        print("Loading NLTK sentence tokenizer...")
        # Download punkt tokenizer if not already present
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
            nltk.download('punkt_tab', quiet=True)

    def extract_facts(self, summaries):
        # Extracts statements (facts) from text summaries using NLTK
        facts = []
        for summary in summaries:
            # Use NLTK to split text into sentences
            sentences = sent_tokenize(summary)
            for sent in sentences:
                facts.append(sent.strip())
        return facts

