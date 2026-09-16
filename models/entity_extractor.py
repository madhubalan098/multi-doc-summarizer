from transformers import pipeline
from collections import Counter

class EntityExtractor:
    def __init__(self):
        print("Loading NER model for entity extraction...")
        # Using a smaller, efficient NER model
        self.ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple", device=-1)
    
    def extract_entities(self, texts):
        """
        Extract named entities (persons, organizations, locations) from texts
        """
        all_entities = {
            'PERSON': [],
            'ORG': [],
            'LOC': [],
            'MISC': []
        }
        
        # Process each text
        for text in texts:
            if not text or len(text.strip()) < 10:
                continue
            
            # Truncate very long texts to avoid memory issues
            text_chunk = text[:5000] if len(text) > 5000 else text
            
            try:
                entities = self.ner_pipeline(text_chunk)
                
                for entity in entities:
                    entity_type = entity['entity_group']
                    entity_text = entity['word'].strip()
                    
                    # Map common entity types
                    if entity_type in ['PER', 'PERSON']:
                        all_entities['PERSON'].append(entity_text)
                    elif entity_type in ['ORG', 'ORGANIZATION']:
                        all_entities['ORG'].append(entity_text)
                    elif entity_type in ['LOC', 'LOCATION', 'GPE']:
                        all_entities['LOC'].append(entity_text)
                    else:
                        all_entities['MISC'].append(entity_text)
            except Exception as e:
                print(f"Error processing text for entities: {e}")
                continue
        
        # Count and sort entities by frequency
        result = {}
        for entity_type, entities_list in all_entities.items():
            if entities_list:
                counter = Counter(entities_list)
                # Get top 15 most common entities
                result[entity_type] = [{'entity': name, 'count': count} 
                                      for name, count in counter.most_common(15)]
        
        return result
