import spacy
import json
import os

nlp = spacy.load("fr_core_news_sm")

data = [
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
    {"sentence": "Le cinéma offre une évasion du quotidien.", "label": 0},
    {"sentence": "Londres est la capitale de l'Angleterre.", "label": 1},
    {"sentence": "Les plages de Rio de Janeiro sont célèbres dans le monde entier.", "label": 1},
    {"sentence": "Tokyo est une ville très animée.", "label": 1},
    {"sentence": "Les montagnes de Vancouver offrent de superbes vues.", "label": 1},
    {"sentence": "Istanbul est située à cheval entre l'Europe et l'Asie.", "label": 1},
    {"sentence": "Les rues de Marrakech sont remplies de couleurs et d'arômes.", "label": 1},
    {"sentence": "Sydney est connue pour son opéra emblématique.", "label": 1},
    {"sentence": "Les plages de Miami attirent de nombreux touristes.", "label": 1},
    {"sentence": "Lima est la capitale du Pérou.", "label": 1},
    {"sentence": "Athènes est une ville chargée d'histoire.", "label": 1},
    {"sentence": "Les étoiles brillent dans le ciel nocturne.", "label": 0},
    {"sentence": "La cuisine italienne est réputée pour ses pâtes.", "label": 0},
    {"sentence": "Les oiseaux chantent tôt le matin.", "label": 0},
    {"sentence": "Le cinéma offre une évasion du quotidien.", "label": 0},
    {"sentence": "Les forêts sont essentielles pour l'écosystème.", "label": 0},
    {"sentence": "La danse est une forme d'expression artistique.", "label": 0},
    {"sentence": "La musique classique apaise l'âme.", "label": 0},
    {"sentence": "Le silence règne dans la bibliothèque.", "label": 0},
    {"sentence": "Les écoles préparent les enfants pour l'avenir.", "label": 0},
    {"sentence": "Les rivières serpentent à travers le paysage.", "label": 0},
    {"sentence": "Barcelone est célèbre pour son architecture unique.", "label": 1},
    {"sentence": "Les ruelles de Florence regorgent d'art.", "label": 1},
    {"sentence": "Les montagnes de Denver sont populaires pour le ski.", "label": 1},
    {"sentence": "Los Angeles est connue pour l'industrie du cinéma.", "label": 1},
    {"sentence": "Les plages de Cancún sont idéales pour la détente.", "label": 1},
    {"sentence": "Venise est surnommée la 'Cité des canaux'.", "label": 1},
    {"sentence": "Las Vegas est célèbre pour ses casinos.", "label": 1},
    {"sentence": "La Havane est la capitale de Cuba.", "label": 1},
    {"sentence": "Édimbourg est riche en histoire.", "label": 1},
    {"sentence": "Les rues de Prague sont pittoresques.", "label": 1},
    {"sentence": "Les étoiles filantes illuminent la nuit.", "label": 0},
    {"sentence": "La mer est calme au coucher du soleil.", "label": 0},
    {"sentence": "La montagne offre des possibilités de randonnée.", "label": 0},
    {"sentence": "La forêt abrite de nombreuses espèces animales.", "label": 0},
    {"sentence": "La musique jazz a une grande influence.", "label": 0},
    {"sentence": "Les fleurs dans le jardin sont magnifiques.", "label": 0},
    {"sentence": "Le café est une boisson appréciée le matin.", "label": 0},
    {"sentence": "Le théâtre est une forme d'art captivante.", "label": 0},
    {"sentence": "La poésie touche les cœurs des lecteurs.", "label": 0},
    {"sentence": "La cuisine chinoise est variée et délicieuse.", "label": 0},
    {"sentence": "Les pyreenees est une grande chaine de montagne.", "label": 1}
]

formatted_data = []

for example in data:
    sentence = example["sentence"]
    doc = nlp(sentence)
    
    tokens = [token.text for token in doc]
    labels = []
    for token in doc:
        if token.ent_type_ == "LOC":  # Vous pouvez adapter cette condition à vos besoins
            labels.append("B-LOC")
        else:
            labels.append("O")
    
    example_data = {"tokens": tokens, "labels": labels}
    formatted_data.append(example_data)

# Créez un répertoire de sortie s'il n'existe pas
output_dir = "datasets_ner"
os.makedirs(output_dir, exist_ok=True)

output_filename = os.path.join(output_dir, "dataset_ner_train.json")

with open(output_filename, "w", encoding="utf-8") as json_file:
    json.dump(formatted_data, json_file, ensure_ascii=False, indent=4)

print(f"Les données ont été exportées au format JSON dans {output_filename}.")