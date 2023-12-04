import spacy

# On charge le modèle 
ner = spacy.load('output/model-last');

content = "Trouve moi le trajet pour aller à Paris alors que je suis à Toulouse"

doc = ner(content);

for ent in doc.ents:
    print(ent.text, ent.label_)