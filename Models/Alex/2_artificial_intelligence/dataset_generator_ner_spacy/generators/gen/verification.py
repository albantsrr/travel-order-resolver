import spacy
from spacy.training.iob_utils import offsets_to_biluo_tags
import json


def check_data(file_path):
    # Charger le modèle spaCy
    nlp = spacy.blank('fr')

    # Charger les données depuis le fichier JSON
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Vérifier chaque phrase et ses annotations
    for text, annotations in data:
        doc = nlp(text)
        entities = annotations['entities']
        try:
            biluo_tags = offsets_to_biluo_tags(doc, entities)
            if '-' in biluo_tags:
                print(f"Problème d'alignement dans : {text}")
                print(f"Entities: {entities}")
                print(f"BILUO tags: {biluo_tags}\n")
        except ValueError as e:
            print(
                f"=======================================================Erreur dans le texte : {text}")
            print(f"Erreur : {e}")


# Chemins des fichiers de données
test_datas = "../../dataset/tests/test_data.json"
train_datas = "../../dataset/train/train_data.json"
val_datas = "../../dataset/validations/val_data.json"

# Effectuer la vérification
check_data(test_datas)
check_data(train_datas)
check_data(val_datas)
