import requests
import random
import json
import nltk
from nltk.corpus import words

nltk.download('words')

# Récupérer la liste des villes de France
response = requests.get("https://geo.api.gouv.fr/communes")
data = response.json()

# Extraire seulement les noms des villes
city_names = [city["nom"] for city in data]

# Créer une liste pour stocker les phrases générées
generated_sentences = []

# Modèles de phrases avec divers temps de conjugaison
phrase_patterns = [
    "Je souhaite prendre le train de {start_city} à {end_city}.",
    "Je préférerai voyager en train de {start_city} à {end_city}.",
    "Je planifie un voyage en train de {start_city} à {end_city}.",
    "Je voudrais réserver un billet de {start_city} à {end_city}.",
    "Je pensais prendre le train de {start_city} à {end_city}.",
    "Je viserai à voyager de {start_city} à {end_city} en train.",
    "Je projetterai de me rendre de {start_city} à {end_city} par train.",
    "Je comptais aller en train de {start_city} à {end_city}.",
    "Nous pensons prendre le train pour aller de {start_city} à {end_city}.",
    "Nous aimerions aller de {start_city} à {end_city} en train.",
    "Nous envisageons un trajet en train de {start_city} à {end_city}.",
    "Nous voudrions acheter des billets de train de {start_city} à {end_city}.",
    "Nous avions l'intention de prendre le train de {start_city} à {end_city}.",
    "Nous étions en train de planifier un voyage de {start_city} à {end_city}.",
    "Nous chercherons à prendre le train de {start_city} à {end_city}.",
    "Nous souhaiterions partir de {start_city} pour {end_city} en train.",
    "Nous aurions préféré voyager en train de {start_city} à {end_city}.",
    "Je serai en train de voyager de {start_city} à {end_city}.",
    "Nous serons en train de prendre le train de {start_city} à {end_city}."
    "Je me dirige vers {end_city} en partant de {start_city} en train.",
    "Je me prépare à aller de {start_city} à {end_city} en chemin de fer.",
    "J'ai l'intention de partir de {start_city} pour atteindre {end_city} par voie ferrée.",
    "Je suis en train de planifier mon itinéraire ferroviaire de {start_city} à {end_city}.",
    "Je me rendrai de {start_city} à {end_city} en prenant le train.",
    "Je me vois déjà voyager en train de {start_city} à {end_city}.",
    "Je suis sur le point de prendre le train entre {start_city} et {end_city}.",
    "Je dois aller en train de {start_city} à {end_city}.",
    "J'envisage de prendre un train direct de {start_city} à {end_city}.",
    "J'ai réservé un billet de train pour aller de {start_city} à {end_city}.",
    "J'ai pour projet de me déplacer en train de {start_city} à {end_city}.",
    "Je dois organiser mon trajet en train de {start_city} à {end_city}.",
    "Je prendrai le prochain train pour {end_city} depuis {start_city}.",
    "Je suis prêt à partir en train de {start_city} à {end_city}.",
    "Je suis en passe de réserver un train de {start_city} à {end_city}.",
    "Je suis décidé à partir en train de {start_city} à {end_city}.",
    "Nous avons prévu de voyager en train de {start_city} à {end_city}.",
    "Nous sommes sur le point de réserver nos billets de {start_city} à {end_city}.",
    "Nous avons déjà acheté nos billets de train de {start_city} à {end_city}."
    "Je m'apprête à prendre le train entre {start_city} et {end_city}.",
    "Je suis en cours de réservation d'un billet de train de {start_city} à {end_city}.",
    "Je me dirigerai vers {end_city} en partant de {start_city} en train.",
    "Je vais bientôt voyager en train de {start_city} à {end_city}.",
    "Je suis en train d'organiser un voyage en train de {start_city} à {end_city}.",
    "Je souhaite m'orienter vers {end_city} en train depuis {start_city}.",
    "Nous avons pour projet de nous rendre en train de {start_city} à {end_city}.",
    "Nous allons prendre un train qui part de {start_city} et arrive à {end_city}.",
    "Je suis sur le point de monter dans un train de {start_city} à {end_city}.",
    "Nous réfléchissons à prendre un train depuis {start_city} vers {end_city}.",
    "Je suis en pleine organisation d'un trajet en train depuis {start_city} jusqu'à {end_city}.",
    "Nous songeons à réserver des places pour un train allant de {start_city} à {end_city}.",
    "Je suis en train de finaliser mes plans pour un trajet en train de {start_city} à {end_city}.",
    "Nous attendons notre train à destination de {end_city} depuis {start_city}.",
    "Je suis prêt à embarquer pour un voyage en train de {start_city} à {end_city}."

]

# Modèles de phrases aléatoires
random_phrase_patterns = [
    "{subject} {verb} {object} {adverb}.",
    "{subject} {verb} {object} parce que c'est {adjective}.",
    "{subject} {adverb} {verb} {object} tout en étant {adjective}.",
    "En général, {subject} {verb} plutôt {adverb}.",
    "Quand {subject} {verb}, c'est souvent {adjective}.",
    "{subject} {verb} {object} {adverb}.",
    "{subject} {verb} {object} et c'est {adjective}.",
    "{subject} {verb} {adverb} {object}."
]

# Exemple de listes de mots
subjects = ["Je", "Tu", "Il", "Nous", "Vous", "Ils"]
verbs = ["mange", "regarde", "écoute", "étudie", "lit", "dort", "explore", "découvre"]
adjectives = ["génial", "inutile", "intéressant", "ennuyeux", "formidable", "étrange"]
adverbs = ["rapidement", "doucement", "sérieusement", "fréquemment", "rarement"]
objects = ["un livre", "une pomme", "la télé", "de la musique", "un film", "un documentaire"]


# Génération de phrase
for i in range(5000):
    # Prendre deux villes aléatoires pour créer une phrase
    start_city = random.choice(city_names)
    end_city = random.choice(city_names)

    if random.random() < 0.8:  # 80% de chance de choisir un modèle lié au train
        pattern = random.choice(phrase_patterns)
        generated_sentence = pattern.format(start_city=start_city, end_city=end_city)
        generated_sentences.append({"sentence": generated_sentence, "label": 1})
    else:  # 20% de chance de choisir un modèle aléatoire
        pattern = random.choice(random_phrase_patterns)
        generated_sentence = pattern.format(
            subject=random.choice(subjects),
            verb=random.choice(verbs),
            adjective=random.choice(adjectives),
            adverb=random.choice(adverbs),
            object=random.choice(objects)
        )
        generated_sentences.append({"sentence": generated_sentence, "label": 0})

# Étape 1 : Charger les données existantes du fichier sentences.json
# with open('sentences.json', 'r', encoding='utf-8') as f:
#     generated_sentences = json.load(f)

# Étape 2 : Lire le fichier sentences.txt et ajouter chaque ligne à generated_sentences avec un label de 0
with open('sentences.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()  # Enlever les espaces et les sauts de ligne en début et en fin de chaque ligne
        if line:  # Vérifier si la ligne n'est pas vide
            random_index = random.randint(0, len(generated_sentences))
            generated_sentences.insert(random_index, {"sentence": line, "label": 0})

# Étape 3 : Sauvegarder le nouveau contenu dans sentences.json
with open('sentences.json', 'w', encoding='utf-8') as f:
    json.dump(generated_sentences, f, ensure_ascii=False, indent=4)
