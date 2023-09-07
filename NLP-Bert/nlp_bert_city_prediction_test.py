import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Charger le tokenizer BERT
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Charger le modèle fine-tuné
model = BertForSequenceClassification.from_pretrained("./models_city_prediction")

# Mettre le modèle en mode évaluation
model.eval()

# Fonction pour prédire si une phrase contient une ville ou non
def predict_city_presence(sentence):
    # Encodage de la phrase
    encoded_input = tokenizer(sentence, padding=True, truncation=True, return_tensors="pt", max_length=128)
    
    # Prédiction avec le modèle
    with torch.no_grad():
        output = model(**encoded_input)
    
    # Récupération de la prédiction (classe 1 pour "Villes" et classe 0 pour "Pas de villes")
    prediction = torch.argmax(output.logits, dim=1).item()
    
    # Vérification de la prédiction
    if prediction == 1:
        return "Il y a une ville dans la phrase."
    else:
        return "Il n'y a pas de ville dans la phrase."

# Exemples de phrases à tester
phrases = [
    "Penses-tu que je puisse me rendre à Port-la-Nouvelle depuis Carcassonne",
    "Les ruelles de Paris regorgent de charme et d'histoire.",
    "La gastronomie italienne est mondialement célèbre pour ses pâtes et ses pizzas.",
    "La ville de Kyoto au Japon est célèbre pour ses temples et ses jardins zen.",
    "Les oiseaux chantent harmonieusement à l'aube dans la forêt tropicale.",
    "Londres est connue pour son mélange unique de culture et d'histoire.",
    "La musique classique est souvent jouée par un orchestre symphonique.",
    "Le cœur historique de Rome est un véritable trésor architectural.",
    "La littérature anglaise a une riche tradition remontant à des siècles.",
    "Le désert du Sahara s'étend sur plusieurs pays d'Afrique.",
    "La ville de Los Angeles est reconnue comme le centre de l'industrie cinématographique.",
    "Pense-tu pouvoir me donner un itinéraire vers Brest en bretagne ?",
    "Comment me rendre a Saint-quentin-des-liziers en France ?",
    "J'aime les quenouilles",
    "Comment faire toulouse paris en train ?",
    "Puis-je me rendre à Moscou en passant par Belgrade",
    "coucou",
    "salut, comment tu-vas ?",
    "Les grande montagne du pérou",
    "Très je trouve que tu t'en sors a merveille Paris"
]

# Faire des prédictions pour chaque phrase
for phrase in phrases:
    result = predict_city_presence(phrase)
    print(f"Phrase : '{phrase}'")
    print(result)
    print()