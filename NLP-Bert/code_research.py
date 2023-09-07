# Séparation des phrases et des étiquettes
sentences = [example["sentence"] for example in data]
labels = [example["label"] for example in data]

# Chargement du tokenizer BERT
tokenizer = BertTokenizer.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")

# Encodage des phrases
encoded_inputs = tokenizer(sentences, padding=True, truncation=True, return_tensors="pt")

# Conversion des étiquettes en identifiants numériques
label_ids = [tokenizer.convert_tokens_to_ids(label) for label in labels]

# Division des données en ensembles d'entraînement et de test
train_inputs, test_inputs, train_labels, test_labels = train_test_split(encoded_inputs["input_ids"], label_ids, test_size=0.15, random_state=42)
train_masks = encoded_inputs["attention_mask"][:len(train_inputs)].clone().detach()
test_masks = encoded_inputs["attention_mask"][len(train_inputs):].clone().detach()

# Création de DataLoader pour l'entraînement
train_dataset = TensorDataset(train_inputs, train_masks, torch.tensor(train_labels))
train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# Chargement du modèle BERT pré-entraîné pour la classification des tokens
model = BertForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")

# Définition de l'optimiseur et de la fonction de perte
optimizer = AdamW(model.parameters(), lr=2e-5)

# Entraînement du modèle
model.train()
for epoch in range(3):  # Réglez le nombre d'époques souhaité
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
    predicted_labels = [torch.argmax(logits, dim=1).tolist() for logits in test_outputs.logits]

# Conversion des identifiants numériques en étiquettes
predicted_labels = [tokenizer.convert_ids_to_tokens(label) for label in predicted_labels]

# Rapport de classification
flat_test_labels = [label for sublist in test_labels for label in sublist]
flat_predicted_labels = [label for sublist in predicted_labels for label in sublist]

report = classification_report(flat_test_labels, flat_predicted_labels)
print(report)

