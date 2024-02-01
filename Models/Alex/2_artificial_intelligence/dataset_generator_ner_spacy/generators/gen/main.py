import csv
import random
import os
import json


# GENERATING DATASET

def load_sentences(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()


def load_cities(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        return [row['COMMUNE'] for row in reader]


def replace_tags_and_annotate(phrase, depart, arrivee):

    len_tag_depart = len('{départ}')
    len_tag_arrivee = len('{arrivée}')

    start_depart = phrase.find('{départ}')
    start_arrivee = phrase.find('{arrivée}')

    phrase_replaced = phrase.replace(
        '{départ}', depart).replace('{arrivée}', arrivee)
    phrase_replaced = phrase_replaced.lower()

    if start_arrivee > start_depart:
        new_start_depart = start_depart
        new_end_depart = new_start_depart + len(depart)
        new_start_arrivee = start_arrivee + len(depart) - len_tag_depart
        new_end_arrivee = new_start_arrivee + len(arrivee)
    else:
        new_start_arrivee = start_arrivee
        new_end_arrivee = new_start_arrivee + len(arrivee)
        new_start_depart = start_depart + len(arrivee) - len_tag_arrivee
        new_end_depart = new_start_depart + len(depart)

    return (phrase_replaced.strip(), {"entities": [(new_start_depart, new_end_depart, "DEPART"), (new_start_arrivee, new_end_arrivee, "ARRIVEE")]})


def generate_dataset(sentences_files, cities_file, output_file, sentences_to_gen=1000):
    communes = load_cities(cities_file)
    ner_data = []

    for sentence_file in sentences_files:
        phrases_patterns = load_sentences(sentence_file)

        for _ in range(sentences_to_gen):
            pattern = random.choice(phrases_patterns)
            depart, arrivee = random.sample(communes, 2)
            ner_phrase = replace_tags_and_annotate(pattern, depart, arrivee)
            ner_data.append(ner_phrase)

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(ner_data, file, ensure_ascii=False, indent=2)


sentences_files = [
    "../src/phrases_question.txt",
    "../src/phrases_imperatives.txt",
    "../src/phrases_conditionnal.txt",
    "../src/phrases_arrival_first.txt"
]

cities_csv = "../src/liste-des-gares.csv"
output_path = "../res/ner-datas.json"

generate_dataset(sentences_files, cities_csv, output_path)

# SPLITTING DATASET

# Load RES files dataset
with open("../res/ner-datas.json", 'r', encoding='utf-8') as file:
    ner_data = json.load(file)

# Shuffle
random.shuffle(ner_data)

# Dividing datas
train_size = int(0.7 * len(ner_data))
val_size = int(0.15 * len(ner_data))
test_size = len(ner_data) - train_size - val_size

train_data = ner_data[:train_size]
val_data = ner_data[train_size:train_size + val_size]
test_data = ner_data[-test_size:]

# Save them
with open('../../dataset/train/train_data.json', 'w', encoding='utf-8') as file:
    json.dump(train_data, file, ensure_ascii=False, indent=2)

with open('../../dataset/validations/val_data.json', 'w', encoding='utf-8') as file:
    json.dump(val_data, file, ensure_ascii=False, indent=2)

with open('../../dataset/tests/test_data.json', 'w', encoding='utf-8') as file:
    json.dump(test_data, file, ensure_ascii=False, indent=2)
