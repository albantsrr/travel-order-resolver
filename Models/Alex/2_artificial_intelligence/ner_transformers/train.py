import spacy
import random
from spacy.util import minibatch, compounding
from spacy.training import Example
from pathlib import Path
import json

# Load camemBERT model


def load_model(model_name="fr_dep_news_trf"):
    return spacy.load(model_name)

# Helper Function to load train and validation data


def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Train function


def train_ner_model(train_data, val_data, model_name="fr_dep_news_trf", output_dir="./trained_model", n_iter=20):
    nlp = load_model(model_name)
    if 'ner' not in nlp.pipe_names:
        ner = nlp.add_pipe('ner', last=True)
    else:
        ner = nlp.get_pipe('ner')

    # Add labels to the NER
    for _, annotations in train_data:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    # Desactivate other pipeline components
    disable_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*disable_pipes):
        optimizer = nlp.resume_training()
        for itn in range(n_iter):
            random.shuffle(train_data)
            losses = {}
            batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                examples = []
                for text, annots in batch:
                    doc = nlp.make_doc(text)
                    example = Example.from_dict(doc, annots)
                    examples.append(example)
                nlp.update(examples, drop=0.5, losses=losses)
            print(f"Iteration {itn} Losses: {losses}")

    # Save the model to a specified directory
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()
    nlp.to_disk(output_dir)
    print(f"Model saved to {output_dir}")


# Path to training and validation data
train_data_file = "./dataset/train/train_data.json"
val_data_file = "./dataset/validations/val_data.json"

# Loading training and validation data
train_data = load_data(train_data_file)
val_data = load_data(val_data_file)

# Training the model
train_ner_model(train_data, val_data, model_name="fr_dep_news_trf",
                output_dir="./trained_model", n_iter=20)
