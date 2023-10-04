import json
import random
import re

# Charger le dataset au format JSON
with open('src/france_cities.json', 'r') as f:
    city_france_json = json.load(f)

# Charger le dataset au format JSON
with open('src/tournure_phrase.json', 'r') as f:
    tournure_phrase_json = json.load(f)

# Initialiser une liste pour stocker les phrases générées
generated_sentences = []

for i in range(1,100):
    # Sélectionnez une ville au hasard
    random_city = random.choice(city_france_json['cities'])
    city_name = random_city['label']

    # Sélectionnez une tournure de phrase au hasard
    random_tournure = random.choice(tournure_phrase_json)
    tournure_phrase = random_tournure['tournure']

    # Combinez la tournure de phrase avec le nom de la ville
    generated_sentence = f"{tournure_phrase} à {city_name}."

    # Affichez la phrase générée
    print(generated_sentence)
     # Ajoutez la phrase générée à la liste
    generated_sentences.append({"sentence": generated_sentence, "label": 1})
    i = i+1

# Enregistrez la liste des phrases générées dans un fichier JSON
with open('src/dataset_predict_city.json', 'w') as outfile:
    json.dump(generated_sentences, outfile, indent=2, ensure_ascii=False, separators=(',', ': '))
