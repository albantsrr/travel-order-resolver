from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

# Ici je passe mon model BERT NLP pre-entrainer avec lequel j'ai entrainer mon models
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
# Ici je passe mon model NER BERT entrainer pour tester une phrase
model = AutoModelForTokenClassification.from_pretrained("./models_extract")

nlp = pipeline("ner", model=model, tokenizer=tokenizer)
example = "Port-la-nouvelle est une ville portuaire."

ner_results = nlp(example)
print(ner_results)