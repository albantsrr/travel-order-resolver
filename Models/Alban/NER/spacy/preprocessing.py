import pandas as pd
import random
from sklearn.model_selection import train_test_split
import spacy
from spacy.tokens import DocBin

# Lire le fichier CSV
df = pd.read_csv('data.csv', delimiter=';')

# On s'assure que toutes les données sont des strings
df['SENTENCE'] = df['SENTENCE'].astype(str)
df['SENTENCE'] = df['SENTENCE'].str.lower()
df['ORIGIN'] = df['ORIGIN'].astype(str)
df['ORIGIN'] = df['ORIGIN'].str.lower()
df['ARRIVAL'] = df['ARRIVAL'].astype(str)
df['ARRIVAL'] = df['ARRIVAL'].str.lower()

df = df[df['ARRIVAL'] != df['ORIGIN']]

# Préprocessing des données
def extract_entities(sentence, origin, arrival):
    entities = []
    if origin in sentence:
        start = sentence.find(origin)
        end = start + len(origin)
        entities.append((start, end, 'ORIGIN'))
    if arrival in sentence:
        start = sentence.find(arrival)
        end = start + len(arrival)
        entities.append((start, end, 'ARRIVAL'))
    return (sentence, {'entities': entities})

datas = [extract_entities(row['SENTENCE'], row['ORIGIN'], row['ARRIVAL']) for index, row in df.iterrows()]

# random.shuffle(datas)

# Séparation en ensembles de données
train_data, test_data = train_test_split(datas, test_size=0.2)
train_data, val_data = train_test_split(train_data, test_size=0.25)


# Fonction pour transformer les données en format spaCy
def create_spacy_data(data, file_name):
    nlp = spacy.blank("fr")
    db = DocBin()
    for text, annotations in data:
        doc = nlp(text)
        ents = []
        for start, end, label in annotations['entities']:
            span = doc.char_span(start, end, label=label)
            if span is not None:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk(file_name)

# Création des fichiers spaCy pour l'entraînement, la validation et le test
create_spacy_data(train_data, "./data/train.spacy")
create_spacy_data(val_data, "./data/val.spacy") 
create_spacy_data(test_data, "./data/test.spacy")
