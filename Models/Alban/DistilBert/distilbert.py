#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 11:02:17 2023

@author: albantsr
"""

import pandas as pd 

# %%
# =============================================================================
# Mise en place du dataframe
# =============================================================================


# Je récupère le dataset 
df = pd.read_json("dataset-bert-classification.json")

sentences = df["sentence"].tolist()
labels = df["label"].tolist()


# =============================================================================
# Séparation des données
# =============================================================================
from sklearn.model_selection import train_test_split

# Séparation en ensembles d'entraînement et de test (80% - 20% par exemple)
train_sentences, test_sentences, train_labels, test_labels = train_test_split(sentences, labels, test_size=0.2, random_state=42)

# Séparation de l'ensemble d'entraînement en ensembles d'entraînement et de validation (80% - 20% des données d'entraînement par exemple)
train_sentences, val_sentences, train_labels, val_labels = train_test_split(train_sentences, train_labels, test_size=0.2, random_state=42)


# =============================================================================
# Tokenisation
# =============================================================================


from transformers import DistilBertTokenizer 

# Je charge le tokeniseur 
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

# Tokenisation des données 
train_encodings = tokenizer(train_sentences, truncation=True, padding=True, max_length=128, return_tensors="pt")
val_encodings = tokenizer(val_sentences, truncation=True, padding=True, max_length=128, return_tensors="pt")
test_encodings = tokenizer(test_sentences, truncation=True, padding=True, max_length=128, return_tensors="pt")


# %%
# =============================================================================
# Création du jeu de donnée avec PyTorch
# =============================================================================
import torch

# On définit une extension de la class Dataset de Pytorch 
class CityDataset(torch.utils.data.Dataset):
    
    # initialisation de la classe 
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    # Retourne un dictionnaire contenant les encoding à l'id idx 
    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item
    
    # Retourne le nombre total d'éléments dans la phrases 
    def __len__(self):
        return len(self.labels)
    
# Création des datasets
train_dataset = CityDataset(train_encodings, train_labels)
val_dataset = CityDataset(val_encodings, val_labels)
test_dataset = CityDataset(test_encodings, test_labels)



# %%
# =============================================================================
# Mise en place du modèle 
# =============================================================================

from transformers import DistilBertForSequenceClassification

print('Mise en place du modèle')

# Charger le modèle avec une tête de classification
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=2)


# %%
# =============================================================================
# On entraine le modèle
# =============================================================================# =============================================================================
from transformers import Trainer, TrainingArguments
import logging

logging.basicConfig(level=logging.INFO)

print("Entrainement du modèle")

# Définir les arguments pour l'entraînement
training_args = TrainingArguments(
    per_device_train_batch_size=8,
    num_train_epochs=3,
    logging_dir='./logs',
    logging_steps=10,
    evaluation_strategy="epoch",
    output_dir='./results'
)

# Initialiser le Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

# Entraîner le modèle
trainer.train()

results = trainer.evaluate()


# %%
# =============================================================================
# Prédiction et metrics
# =============================================================================

predictions = trainer.predict(test_dataset)
predicted_labels = predictions.predictions.argmax(axis=1)

from sklearn.metrics import accuracy_score, classification_report

print("Training Loss:", training_loss)

print("Validation Loss:", results["eval_loss"])
print("Accuracy:", accuracy_score(test_labels, predicted_labels))
print(classification_report(test_labels, predicted_labels))




