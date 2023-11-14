import pandas as pd
import random
from sklearn.model_selection import train_test_split
import spacy
from spacy.tokens import DocBin

# Lire le fichier CSV
df = pd.read_csv('data.csv', delimiter=';')


# On s'assure que toutes les données sont des strings
df['SENTENCE'] = df['SENTENCE'].astype(str)
df['ORIGIN'] = df['ORIGIN'].astype(str)
df['ARRIVAL'] = df['ARRIVAL'].astype(str)

# Préprocessing des 
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


random.shuffle(datas)

train_data, test_data = train_test_split(datas, test_size=0.2)
train_data, val_data = train_test_split(train_data, test_size=0.25)


# Préprocessing des données => voir la doc. 
nlp = spacy.blank("fr")
training_data = train_data
db = DocBin()
for text, annotations in training_data:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations['entities']:
        span = doc.char_span(start, end, label=label)
        ents.append(span)
    doc.ents = ents
    db.add(doc)
db.to_disk("./data/train.spacy")


testing_data = test_data
db = DocBin()
for text, annotations in training_data:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations['entities']:
        span = doc.char_span(start, end, label=label)
        if span is not None:
            ents.append(span)
    doc.ents = ents
    db.add(doc)
db.to_disk("./data/test.spacy")
