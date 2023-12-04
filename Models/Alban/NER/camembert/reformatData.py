import pandas as pd
from sklearn.model_selection import train_test_split
import json


df = pd.read_csv('../../../Data_Generator/dataset_generator/generate_sentence.csv', sep=';')
df = df[~df['ORIGIN'].str.contains(' ', na=False)]

def convert_to_bio(row):
    sentence = row['SENTENCE'].split();
    origin = str(row['ORIGIN']) if pd.notnull(row['ORIGIN']) else ''
    arrival = str(row['ARRIVAL']) if pd.notnull(row['ARRIVAL']) else ''

    
    labels = ['O'] * len(sentence)
    for i,  word in enumerate(sentence):
        if word == origin:
            labels[i] = 'B-ORIGIN'
        elif word == arrival:
            labels[i] = 'B-ARRIVAL'
    return {'tokens': sentence, 'ner_tags': labels}

json_data = df.apply(convert_to_bio, axis=1).tolist();
    
with open('ner_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)
