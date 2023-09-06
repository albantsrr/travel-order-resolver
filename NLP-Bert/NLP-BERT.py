import torch
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Chargement du jeu de données
dataset = [
   {"sentence": "Paris est la capitale de la France.", "label": 1},
    {"sentence": "Les montagnes sont belles en Suisse.", "label": 1},
    {"sentence": "Le chien court dans le jardin.", "label": 0},
    {"sentence": "New York est une grande ville américaine.", "label": 1},
    {"sentence": "Les oiseaux chantent dans le parc.", "label": 0},
    {"sentence": "Rome est une ville historique.", "label": 1},
    {"sentence": "Les plages de Bali sont magnifiques.", "label": 1},
    {"sentence": "Les montagnes du Népal sont impressionnantes.", "label": 1},
    {"sentence": "Le chat dort sur le canapé.", "label": 0},
    {"sentence": "Berlin est la capitale de l'Allemagne.", "label": 1},
    {"sentence": "Les étoiles brillent la nuit.", "label": 0},
    {"sentence": "Marseille est une ville portuaire.", "label": 1},
    {"sentence": "Bordeaux est réputée pour son vin.", "label": 1},
    {"sentence": "Le soleil brille à Nice.", "label": 1},
    {"sentence": "Les montagnes du Jura sont magnifiques.", "label": 0},
    {"sentence": "Strasbourg est le siège du Parlement européen.", "label": 1},
    {"sentence": "Les plages de Cannes attirent de nombreux touristes.", "label": 1},
    {"sentence": "Toulouse est connue comme la ville rose.", "label": 1},
    {"sentence": "Lyon est célèbre pour sa cuisine.", "label": 1},
    {"sentence": "Les rues de Paris sont pleines de charme.", "label": 1},
    {"sentence": "Les Alpes françaises sont populaires pour le ski.", "label": 0},
    {"sentence": "Nantes est située sur la Loire.", "label": 1},
    {"sentence": "Les plages de Biarritz sont idéales pour le surf.", "label": 1},
    {"sentence": "Avignon est célèbre pour son festival de théâtre.", "label": 1},
    {"sentence": "Rennes est la capitale de la Bretagne.", "label": 1},
    {"sentence": "Lille est connue pour sa cuisine délicieuse.", "label": 1},
    {"sentence": "Les montagnes des Vosges offrent de superbes randonnées.", "label": 0},
    {"sentence": "Marseille est la deuxième plus grande ville de France.", "label": 1},
    {"sentence": "Les plages de La Rochelle sont charmantes.", "label": 1},
    {"sentence": "Nîmes est célèbre pour ses arènes romaines.", "label": 1},
    {"sentence": "Le Havre est un important port maritime.", "label": 1},
    {"sentence": "Les quais de Bordeaux sont pittoresques.", "label": 1},
    {"sentence": "Les collines de la Drôme sont magnifiques.", "label": 0},
    {"sentence": "Lyon est également connue pour ses traboules.", "label": 1},
    {"sentence": "Les plages de Normandie sont idéales pour la détente.", "label": 1},
    {"sentence": "Biarritz est une destination prisée des surfeurs.", "label": 1},
    {"sentence": "Limoges est célèbre pour sa porcelaine.", "label": 1},
    {"sentence": "Les quais de Rouen sont animés en été.", "label": 1},
    {"sentence": "Les montagnes du Massif central sont majestueuses.", "label": 0},
    {"sentence": "Toulouse est également connue comme la ville de l'aérospatiale.", "label": 1},
    {"sentence": "Les plages de la Côte d'Azur attirent les vacanciers du monde entier.", "label": 1},
    {"sentence": "Les fleurs dans le jardin sont magnifiques.", "label": 0},
    {"sentence": "La cuisine française est célèbre dans le monde entier.", "label": 0},
    {"sentence": "L'hiver apporte de la neige dans certaines régions.", "label": 0},
    {"sentence": "Les étoiles brillent la nuit.", "label": 0},
    {"sentence": "Le café est une boisson populaire le matin.", "label": 0},
    {"sentence": "Les océans couvrent une grande partie de la Terre.", "label": 0},
    {"sentence": "La musique classique est apaisante.", "label": 0},
    {"sentence": "Les arbres perdent leurs feuilles en automne.", "label": 0},
    {"sentence": "La montagne offre des possibilités de randonnée.", "label": 0},
    {"sentence": "Les écoles préparent les enfants pour l'avenir.", "label": 0},
    {"sentence": "Le théâtre est un art fascinant.", "label": 0},
    {"sentence": "Les oiseaux chantent joyeusement le matin.", "label": 0},
    {"sentence": "La littérature classique a une grande influence.", "label": 0},
    {"sentence": "Le ciel est clair et sans nuages.", "label": 0},
    {"sentence": "Les forêts sont un écosystème important.", "label": 0},
    {"sentence": "La danse est une forme d'expression artistique.", "label": 0},
    {"sentence": "Les rivières serpentent à travers le paysage.", "label": 0},
    {"sentence": "Le silence règne dans la bibliothèque.", "label": 0},
    {"sentence": "Les étoiles filantes illuminent la nuit.", "label": 0},
    {"sentence": "Le cinéma offre une évasion du quotidien.", "label": 0}
]

# Séparation des phrases et des étiquettes
sentences = [example["sentence"] for example in dataset]
labels = [example["label"] for example in dataset]

# Chargement du tokenizer BERT
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Encodage des phrases
encoded_inputs = tokenizer(sentences, padding=True, truncation=True, return_tensors="pt", max_length=128)

# Division des données en ensembles d'entraînement, de validation et de test
train_inputs, test_inputs, train_labels, test_labels = train_test_split(encoded_inputs["input_ids"], labels, test_size=0.15, random_state=42)
train_masks = torch.tensor(encoded_inputs["attention_mask"][:len(train_inputs)])
test_masks = torch.tensor(encoded_inputs["attention_mask"][len(train_inputs):])

# Création de DataLoader pour l'entraînement
train_dataset = TensorDataset(train_inputs, train_masks, torch.tensor(train_labels))
train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# Chargement du modèle BERT pré-entraîné pour la classification binaire
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

# Définition de l'optimiseur et de la fonction de perte
optimizer = AdamW(model.parameters(), lr=2e-5)
loss_fn = torch.nn.CrossEntropyLoss()

# Entraînement du modèle
model.train()
for epoch in range(10):
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

model.save_pretrained("./")

# Vous pouvez maintenant utiliser votre modèle fine-tuné pour prédire la présence de noms de villes dans de nouvelles phrases.
