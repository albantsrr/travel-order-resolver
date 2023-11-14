    # -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
from transformers import AutoTokenizer, AutoModelForTokenClassification, Trainer, TrainingArguments
from transformers import pipeline
from transformers import AutoModel
from datasets import Dataset
import json


data = pd.read_json("dataset.json");

data = data[['tokens', 'ner_tags']]

dataset = Dataset.from_pandas(data)

tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner")
model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner")

label_map = {'O': 0, 'B-ORIGIN': 1, 'B-ARRIVAL': 2 }
def tokenize_and_align_labels(examples):
    # Tokenisez les entrées textuelles.
    tokenized_inputs = tokenizer(examples["tokens"], truncation=True, padding='max_length', is_split_into_words=True)
    
    labels = []
    for i, label in enumerate(examples["ner_tags"]):
        # Obtenez les ID des mots pour l'alignement des étiquettes.
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []
        
        for word_idx in word_ids:
            # Pour les tokens spéciaux comme [CLS], [SEP], [PAD], etc., nous utilisons -100.
            if word_idx is None or word_idx == previous_word_idx:
                label_ids.append(-100)
            else:
                # Convertissez les étiquettes textuelles en étiquettes numériques.
                label_ids.append(label_map[label[word_idx]])
            previous_word_idx = word_idx
        
        labels.append(label_ids)
    
    # Ajoutez les étiquettes numériques aux sorties tokenisées.
    tokenized_inputs["labels"] = labels
    return tokenized_inputs

tokenized_dataset = dataset.map(tokenize_and_align_labels, batched=True)

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=3,
    weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
)

trainer.train()

nlp = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")
result = nlp("J'aimerais me rendre de Paris à Toulouse")
print(result)