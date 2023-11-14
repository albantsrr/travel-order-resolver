import pandas as pd

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

training_data = [extract_entities(row['SENTENCE'], row['ORIGIN'], row['ARRIVAL']) for index, row in df.iterrows()]

print(training_data[:3])
