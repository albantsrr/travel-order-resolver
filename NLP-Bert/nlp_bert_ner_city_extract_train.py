import torch
from transformers import BertTokenizer, BertForTokenClassification, TrainingArguments, Trainer, DataCollatorForTokenClassification
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
import json

# Charger le dataset au format JSON
with open('datasets_ner/dataset_ner_train.json', 'r') as f:
    data = json.load(f)

# Séparer les tokens et les labels du dataset
tokens_list = [example["tokens"] for example in data]
labels_list = [example["labels"] for example in data]

# Charger le tokenizer BERT
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Créer des étiquettes au format BIO (Begin, Inside, Outside)
formatted_labels = []
for labels in labels_list:
    formatted_labels.append(["B-" + label if label != "O" else label for label in labels])


sentences = [" ".join(tokens) for tokens in tokens_list]

encoded_inputs = tokenizer(sentences, padding=True, truncation=True, return_tensors="pt")
input_ids = encoded_inputs["input_ids"]
attention_mask = encoded_inputs["attention_mask"]

# Séparer les données en ensembles d'entraînement et de validation
train_inputs, val_inputs, train_labels, val_labels = train_test_split(input_ids, formatted_labels, test_size=0.2, random_state=42)
train_masks, val_masks, _, _ = train_test_split(attention_mask, input_ids, test_size=0.2, random_state=42)

# # Créer un dictionnaire de correspondance entre les étiquettes et les identifiants
label_to_id = {
    "O": 0,
    "B-LOC": 1,
}

# Convertir les étiquettes au format BIO en identifiants d'étiquettes
train_labels = [
    [label_to_id[label] for label in train_labels[0]]
]

train_labels = [torch.tensor(label_ids) for label_ids in train_labels]


train_dataset = TensorDataset(train_inputs, train_masks, train_labels)
val_dataset = TensorDataset(val_inputs, val_masks, val_labels)

# Charger le modèle BERT pour la classification de token
model = BertForTokenClassification.from_pretrained("bert-base-uncased", num_labels=2)  # Assurez-vous que num_labels est correct

# Préparer le data collator
data_collator = DataCollatorForTokenClassification(tokenizer)

# Définir les arguments d'entraînement
training_args = TrainingArguments(
    output_dir='./ner_model',
    num_train_epochs=8,
    per_device_train_batch_size=32,
    evaluation_strategy="epoch",
    save_total_limit=2,
)

# Créer un objet Trainer pour l'entraînement
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

# Entraîner le modèle
trainer.train()

# Enregistrer le modèle entraîné
trainer.save_model()