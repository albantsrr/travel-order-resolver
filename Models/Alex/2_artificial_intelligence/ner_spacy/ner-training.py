import spacy
import random
import json

from pathlib import Path

from spacy.training import Example
from spacy.util import minibatch
from spacy.scorer import Scorer
from spacy.training import Example

from sklearn.metrics import confusion_matrix, classification_report

# ? LOADING DATAS


def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


# ? TRAINING MODEL PROCESSING
def train_ner_model(train_data, val_data, model=None, output_dir=None, n_iter=100):
    # Load an existing model or create a new one
    if model is not None:
        nlp = spacy.load(model)  # Load an existing model
        print(f"===> Loading model '{model}'")
    else:
        nlp = spacy.blank('fr')  # Create a new blank model (French)
        print("===> Creating a new blank model")

    # Add the NER component to the pipeline if it's not already there
    if 'ner' not in nlp.pipe_names:
        ner = nlp.add_pipe('ner', last=True)
    else:
        ner = nlp.get_pipe('ner')

    # Add labels to the NER
    for _, annotations in train_data:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    # Disable other pipeline components for training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(train_data)
            losses = {}

            # Batch the examples and process them
            for batch in spacy.util.minibatch(train_data, size=2):
                examples = [Example.from_dict(nlp.make_doc(
                    text), annots) for text, annots in batch]
                nlp.update(examples, drop=0.5, losses=losses, sgd=optimizer)

            print(f"===> Loss at iteration {itn}: {losses['ner']}")

    # Test the model on validation data
    for text, annots in val_data:
        doc = nlp(text)
        # print(f"===> Text: {text}")
        # for ent in doc.ents:
        #     print(f"{ent.label_}: {ent.text}")

    # Save the model to a specified directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print(f"===> Model saved to {output_dir}")


# ? DATA FILES
train_data_file = "./dataset/train/train_data.json"
val_data_file = "./dataset/validations/val_data.json"

# ? LOADING DATAS
train_data = load_data(train_data_file)
val_data = load_data(val_data_file)

# ? TRAINING MODEL
train_ner_model(train_data, val_data, model="fr_core_news_lg",
                output_dir="./model_output", n_iter=50)
