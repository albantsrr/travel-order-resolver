import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, TensorDataset
from torch.optim.adamw import AdamW
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import json
# Chargement du jeu de données
with open('datasets/dataset-bert-classification.json', 'r') as f:
    dataset = json.load(f)

# Séparation des phrases et des étiquettes
sentences = [example["sentence"] for example in dataset]
labels = [example["label"] for example in dataset]

# Chargement du tokenizer BERT
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Encodage des phrases
encoded_inputs = tokenizer(sentences, padding=True, truncation=True, return_tensors="pt", max_length=128)

# Division des données en ensembles d'entraînement, de validation et de test
train_inputs, test_inputs, train_labels, test_labels = train_test_split(encoded_inputs["input_ids"], labels, test_size=0.20, random_state=42)
train_masks = encoded_inputs["attention_mask"][:len(train_inputs)].clone().detach()
test_masks = encoded_inputs["attention_mask"][len(train_inputs):].clone().detach()

# Création de DataLoader pour l'entraînement
train_dataset = TensorDataset(train_inputs, train_masks, torch.tensor(train_labels))
train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# Chargement du modèle BERT pré-entraîné pour la classification binaire
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)
model.config.num_labels = 2

# Définition de l'optimiseur et de la fonction de perte
optimizer = AdamW(model.parameters(), lr=2e-5)
loss_fn = torch.nn.CrossEntropyLoss()

# Entraînement du modèle
model.train()
for epoch in range(4):
    for batch in train_dataloader:
        optimizer.zero_grad()
        inputs, masks, labels = batch
        outputs = model(input_ids=inputs, attention_mask=masks, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()

# Évaluation du modèle
model.eval()
with torch.no_grad():
    test_outputs = model(input_ids=test_inputs, attention_mask=test_masks)
    predicted_labels = torch.argmax(test_outputs.logits, dim=1).tolist()

accuracy = accuracy_score(test_labels, predicted_labels)
report = classification_report(test_labels, predicted_labels, target_names=["Pas de villes", "Villes"])

print(f"Accuracy: {accuracy}")
print(report)

model.save_pretrained("./models_city_prediction")
