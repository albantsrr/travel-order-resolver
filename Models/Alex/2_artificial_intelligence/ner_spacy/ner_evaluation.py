import spacy
import random
import json

from pathlib import Path

from spacy.training import Example
from spacy.util import minibatch
from spacy.scorer import Scorer
from spacy.training import Example

from sklearn.metrics import confusion_matrix, classification_report


def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


# ? DATA FILES
train_data_file = "./dataset/train/train_data.json"
val_data_file = "./dataset/validations/val_data.json"

# ? LOADING DATAS
train_data = load_data(train_data_file)
val_data = load_data(val_data_file)

# ? MODEL METRICS


def load_data_for_evaluation(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    eval_data = []
    for text, entities in data:
        entities_list = []
        for item in entities:
            if len(item) >= 3:
                start, end, label = item[:3]
                try:
                    start = int(start)
                    end = int(end)
                    entities_list.append((start, end, label))
                except ValueError:
                    continue
        eval_data.append((text, {"entities": entities_list}))
    return eval_data


# Confusion Matrix
def evaluate_model(model_path, eval_data):
    nlp = spacy.load(model_path)
    scorer = Scorer()

    examples = []  # Liste pour stocker les objets Example

    for text, annot in eval_data:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annot)
        predicted_doc = nlp(text)
        examples.append(Example(predicted_doc, example.reference))

    scores = scorer.score(examples)  # Calcul des scores
    return scores


eval_data = load_data_for_evaluation(val_data_file)
model_path = "./model_output"
scores = evaluate_model(model_path, eval_data)

print("===> PRECISION:", scores['ents_p'])
print("===> RECALL:", scores['ents_r'])
print("===> F1 SCORE:", scores['ents_f'])
