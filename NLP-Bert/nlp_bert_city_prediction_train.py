import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, TensorDataset
from torch.optim.adamw import AdamW
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Chargement du jeu de données
dataset = [
    {"sentence": "Paris est la capitale de la France.", "annonted_sentence": "<ville>Paris</ville> est la capitale de la France." ,"label": 1},
    {"sentence": "Les montagnes sont belles en Suisse.", "annotated_sentence": "Les montagnes sont belles en Suisse.", "label": 0},
    {"sentence": "Le chien court dans le jardin.", "annotated_sentence": "Le chien court dans le jardin.", "label": 0},
    {"sentence": "New York est une grande ville américaine.", "annotated_sentence": "<ville>New York</ville> est une grande ville américaine.", "label": 1},
    {"sentence": "Les oiseaux chantent dans le parc.", "annotated_sentence": "Les oiseaux chantent dans le parc.", "label": 0},
    {"sentence": "Rome est une ville historique.", "annotated_sentence": "<ville>Rome</ville> est une ville historique.", "label": 1},
    {"sentence": "Les plages de Bali sont magnifiques.", "annotated_sentence": "Les plages de <ville>Bali</ville> sont magnifiques.", "label": 1},
    {"sentence": "Les montagnes du Népal sont impressionnantes.", "annotated_sentence": "Les montagnes du <ville>Népal</ville> sont impressionnantes.", "label": 1},
    {"sentence": "Le chat dort sur le canapé.", "annotated_sentence": "Le chat dort sur le canapé.", "label": 0},
    {"sentence": "Berlin est la capitale de l'Allemagne.", "annotated_sentence": "<ville>Berlin</ville> est la capitale de l'Allemagne.", "label": 1},
    {"sentence": "Les étoiles brillent la nuit.", "annotated_sentence": "Les étoiles brillent la nuit.", "label": 0},
    {"sentence": "Marseille est une ville portuaire.", "annotated_sentence": "<ville>Marseille</ville> est une ville portuaire.", "label": 1},
    {"sentence": "Bordeaux est réputée pour son vin.", "annotated_sentence": "<ville>Bordeaux</ville> est réputée pour son vin.", "label": 1},
    {"sentence": "Le soleil brille à Nice.", "annotated_sentence": "Le soleil brille à <ville>Nice</ville>.", "label": 1},
    {"sentence": "Les montagnes du Jura sont magnifiques.", "annotated_sentence": "Les montagnes du Jura sont magnifiques.", "label": 0},
    {"sentence": "Strasbourg est le siège du Parlement européen.", "annotated_sentence": "<ville>Strasbourg</ville> est le siège du Parlement européen.", "label": 1},
    {"sentence": "Les plages de Cannes attirent de nombreux touristes.", "annotated_sentence": "Les plages de <ville>Cannes</ville> attirent de nombreux touristes.", "label": 1},
    {"sentence": "Toulouse est connue comme la ville rose.", "annotated_sentence": "<ville>Toulouse</ville> est connue comme la ville rose.", "label": 1},
    {"sentence": "Lyon est célèbre pour sa cuisine.", "annotated_sentence": "<ville>Lyon</ville> est célèbre pour sa cuisine.", "label": 1},
    {"sentence": "Les rues de Paris sont pleines de charme.", "annotated_sentence": "<ville>Paris</ville> est célèbre pour sa cuisine.", "label": 1},
    {"sentence": "Les Alpes françaises sont populaires pour le ski.", "annotated_sentence": "Les Alpes françaises sont populaires pour le ski.", "label": 0},
    {"sentence": "Nantes est située sur la Loire.", "annotated_sentence": "<ville>Nantes</ville> est située sur la Loire.", "label": 1},
    {"sentence": "Les plages de Biarritz sont idéales pour le surf.", "annotated_sentence": "Les plages de <ville>Biarritz</ville> sont idéales pour le surf.", "label": 1},
    {"sentence": "Avignon est célèbre pour son festival de théâtre.", "annotated_sentence": "<ville>Avignon</ville> est célèbre pour son festival de théâtre.", "label": 1},
    {"sentence": "Rennes est la capitale de la Bretagne.", "annotated_sentence": "<ville>Rennes</ville> est la capitale de la Bretagne.", "label": 1},
    {"sentence": "Lille est connue pour sa cuisine délicieuse.", "annotated_sentence": "<ville>Lille</ville> est connue pour sa cuisine délicieuse.", "label": 1},
    {"sentence": "Les montagnes des Vosges offrent de superbes randonnées.", "annotated_sentence": "Les montagnes des Vosges offrent de superbes randonnées.", "label": 0},
    {"sentence": "Marseille est la deuxième plus grande ville de France.", "annotated_sentence": "<ville>Marseille</ville> est la deuxième plus grande ville de France.", "label": 1},
    {"sentence": "Les plages de La Rochelle sont charmantes.", "annotated_sentence": "Les plages de <ville>La Rochelle</ville> sont charmantes.", "label": 1},
    {"sentence": "Nîmes est célèbre pour ses arènes romaines.", "annotated_sentence": "<ville>Nîmes</ville> est célèbre pour ses arènes romaines.", "label": 1},
    {"sentence": "Le Havre est un important port maritime.", "annotated_sentence": "<ville>Le Havre</ville> est un important port maritime.", "label": 1},
    {"sentence": "Les quais de Bordeaux sont pittoresques.", "annotated_sentence": "Les quais de <ville>Bordeaux</ville> sont pittoresques.", "label": 1},
    {"sentence": "Les collines de la Drôme sont magnifiques.", "annotated_sentence": "Les collines de la Drôme sont magnifiques.", "label": 0},
    {"sentence": "Lyon est également connue pour ses traboules.", "annotated_sentence": "<ville>Lyon</ville> est également connue pour ses traboules.", "label": 1},
    {"sentence": "Les plages de Normandie sont idéales pour la détente.", "annotated_sentence": "Les plages de <ville>Normandie</ville> sont idéales pour la détente.", "label": 0},
    {"sentence": "Biarritz est une destination prisée des surfeurs.", "annotated_sentence": "<ville>Biarritz</ville> est une destination prisée des surfeurs.", "label": 1},
    {"sentence": "Limoges est célèbre pour sa porcelaine.", "annotated_sentence": "<ville>Limoges</ville> est célèbre pour sa porcelaine.", "label": 1},
    {"sentence": "Les quais de Rouen sont animés en été.", "annotated_sentence": "Les quais de <ville>Rouen</ville> sont animés en été.", "label": 1},
    {"sentence": "Les montagnes du Massif central sont majestueuses.", "annotated_sentence": "Les montagnes du Massif central sont majestueuses.", "label": 0},
    {"sentence": "Toulouse est également connue comme la ville de l'aérospatiale.", "annotated_sentence": "<ville>Toulouse</ville> est également connue comme la ville de l'aérospatiale.", "label": 1},
    {"sentence": "Les plages de la Côte d'Azur attirent les vacanciers du monde entier.", "annotated_sentence": "Les plages de la Côte d'Azur attirent les vacanciers du monde entier.", "label": 0},
    {"sentence": "Les fleurs dans le jardin sont magnifiques.", "annotated_sentence": "Les fleurs dans le jardin sont magnifiques.", "label": 0},
    {"sentence": "La cuisine française est célèbre dans le monde entier.", "annotated_sentence": "La cuisine française est célèbre dans le monde entier.", "label": 0},
    {"sentence": "L'hiver apporte de la neige dans certaines régions.", "annotated_sentence": "L'hiver apporte de la neige dans certaines régions.", "label": 0},
    {"sentence": "Les étoiles brillent la nuit.", "annotated_sentence": "Les étoiles brillent la nuit.", "label": 0},
    {"sentence": "Le café est une boisson populaire le matin.", "annotated_sentence": "Le café est une boisson populaire le matin.", "label": 0},
    {"sentence": "Les océans couvrent une grande partie de la Terre.", "annotated_sentence": "Les océans couvrent une grande partie de la Terre.", "label": 0},
    {"sentence": "La musique classique est apaisante.", "annotated_sentence": "La musique classique est apaisante.", "label": 0},
    {"sentence": "Les arbres perdent leurs feuilles en automne.", "annotated_sentence": "Les arbres perdent leurs feuilles en automne.", "label": 0},
    {"sentence": "La montagne offre des possibilités de randonnée.", "annotated_sentence": "La montagne offre des possibilités de randonnée.", "label": 0},
    {"sentence": "Les écoles préparent les enfants pour l'avenir.", "annotated_sentence": "Les écoles préparent les enfants pour l'avenir.", "label": 0},
    {"sentence": "Le théâtre est un art fascinant.", "annotated_sentence": "Le théâtre est un art fascinant.", "label": 0},
    {"sentence": "Les oiseaux chantent joyeusement le matin.", "annotated_sentence": "Les oiseaux chantent joyeusement le matin.", "label": 0},
    {"sentence": "La littérature classique a une grande influence.", "annotated_sentence": "La littérature classique a une grande influence.", "label": 0},
    {"sentence": "Le ciel est clair et sans nuages.", "annotated_sentence": "Le ciel est clair et sans nuages.", "label": 0},
    {"sentence": "Les forêts sont un écosystème important.", "annotated_sentence": "Les forêts sont un écosystème important.", "label": 0},
    {"sentence": "La danse est une forme d'expression artistique.", "annotated_sentence": "La danse est une forme d'expression artistique.", "label": 0},
    {"sentence": "Les rivières serpentent à travers le paysage.", "annotated_sentence": "Les rivières serpentent à travers le paysage.", "label": 0},
    {"sentence": "Le silence règne dans la bibliothèque.", "annotated_sentence": "Le silence règne dans la bibliothèque.", "label": 0},
    {"sentence": "Les étoiles filantes illuminent la nuit.", "annotated_sentence": "Les étoiles filantes illuminent la nuit.", "label": 0},
    {"sentence": "Le cinéma offre une évasion du quotidien.", "annotated_sentence": "Le cinéma offre une évasion du quotidien.", "label": 0},
    {"sentence": "Londres est la capitale de l'Angleterre.", "annotated_sentence": "<ville>Londres</ville> est la capitale de l'Angleterre.", "label": 1},
    {"sentence": "Les plages de Rio de Janeiro sont célèbres dans le monde entier.", "annotated_sentence": "Les plages de <ville>Rio de Janeiro</ville> sont célèbres dans le monde entier.", "label": 1},
    {"sentence": "Tokyo est une ville très animée.", "annotated_sentence": "<ville>Tokyo</ville> est une ville très animée.", "label": 1},
    {"sentence": "Les montagnes de Vancouver offrent de superbes vues.", "annotated_sentence": "Les montagnes de <ville>Vancouver</ville> offrent de superbes vues.", "label": 1},
    {"sentence": "Istanbul est située à cheval entre l'Europe et l'Asie.", "annotated_sentence": "<ville>Istanbul</ville> est située à cheval entre l'Europe et l'Asie.", "label": 1},
    {"sentence": "Les rues de Marrakech sont remplies de couleurs et d'arômes.", "annotated_sentence": "Les rues de <ville>Marrakech</ville> sont remplies de couleurs et d'arômes.", "label": 1},
    {"sentence": "Sydney est connue pour son opéra emblématique.", "annotated_sentence": "<ville>Sydney</ville> est connue pour son opéra emblématique.", "label": 1},
    {"sentence": "Les plages de Miami attirent de nombreux touristes.", "annotated_sentence": "Les plages de <ville>Miami</ville> attirent de nombreux touristes.", "label": 1},
    {"sentence": "Lima est la capitale du Pérou.", "annotated_sentence": "<ville>Lima</ville> est la capitale du Pérou.", "label": 1},
    {"sentence": "Athènes est une ville chargée d'histoire.", "annotated_sentence": "<ville>Athènes</ville> est une ville chargée d'histoire.", "label": 1},
    {"sentence": "Les étoiles brillent dans le ciel nocturne.", "annotated_sentence": "Les étoiles brillent dans le ciel nocturne.", "label": 0},
    {"sentence": "La cuisine italienne est réputée pour ses pâtes.", "annotated_sentence": "La cuisine italienne est réputée pour ses pâtes.", "label": 0},
    {"sentence": "Les oiseaux chantent tôt le matin.", "annotated_sentence": "Les oiseaux chantent tôt le matin.", "label": 0},
    {"sentence": "Le cinéma offre une évasion du quotidien.", "annotated_sentence": "Le cinéma offre une évasion du quotidien.", "label": 0},
    {"sentence": "Les forêts sont essentielles pour l'écosystème.", "annotated_sentence": "Les forêts sont essentielles pour l'écosystème.", "label": 0},
    {"sentence": "La danse est une forme d'expression artistique.", "annotated_sentence": "La danse est une forme d'expression artistique.", "label": 0},
    {"sentence": "La musique classique apaise l'âme.", "annotated_sentence": "La musique classique apaise l'âme.", "label": 0},
    {"sentence": "Le silence règne dans la bibliothèque.", "annotated_sentence": "Le silence règne dans la bibliothèque.", "label": 0},
    {"sentence": "Les écoles préparent les enfants pour l'avenir.", "annotated_sentence": "Les écoles préparent les enfants pour l'avenir.", "label": 0},
    {"sentence": "Les rivières serpentent à travers le paysage.", "annotated_sentence": "Les rivières serpentent à travers le paysage.", "label": 0},
    {"sentence": "Barcelone est célèbre pour son architecture unique.", "annotated_sentence": "<ville>Barcelone</ville> est célèbre pour son architecture unique.", "label": 1},
    {"sentence": "Les ruelles de Florence regorgent d'art.", "annotated_sentence": "Les ruelles de <ville>Florence</ville> regorgent d'art.", "label": 1},
    {"sentence": "Les montagnes de Denver sont populaires pour le ski.", "annotated_sentence": "Les montagnes de <ville>Denver</ville> sont populaires pour le ski.", "label": 1},
    {"sentence": "Los Angeles est connue pour l'industrie du cinéma.", "annotated_sentence": "<ville>Los Angeles</ville> est connue pour l'industrie du cinéma.", "label": 1},
    {"sentence": "Les plages de Cancún sont idéales pour la détente.", "annotated_sentence": "Les plages de <ville>Cancún</ville> sont idéales pour la détente.", "label": 1},
    {"sentence": "Venise est surnommée la 'Cité des canaux'.", "annotated_sentence": "<ville>Venise</ville> est surnommée la 'Cité des canaux'.", "label": 1},
    {"sentence": "Las Vegas est célèbre pour ses casinos.", "annotated_sentence": "<ville>Las Vegas</ville> est célèbre pour ses casinos.", "label": 1},
    {"sentence": "La Havane est la capitale de Cuba.", "annotated_sentence": "<ville>La Havane</ville> est la capitale de Cuba.", "label": 1},
    {"sentence": "Édimbourg est riche en histoire.", "annotated_sentence": "<ville>Édimbourg</ville> est riche en histoire.", "label": 1},
    {"sentence": "Les rues de Prague sont pittoresques.", "annotated_sentence": "Les rues de <ville>Prague</ville> sont pittoresques.", "label": 1},
    {"sentence": "Les étoiles filantes illuminent la nuit.", "annotated_sentence": "Les étoiles filantes illuminent la nuit.", "label": 0},
    {"sentence": "La mer est calme au coucher du soleil.", "annotated_sentence": "La mer est calme au coucher du soleil.", "label": 0},
    {"sentence": "La montagne offre des possibilités infinies pour les randonneurs et les alpinistes.", "annotated_sentence": "La montagne offre des possibilités infinies pour les randonneurs et les alpinistes.", "label": 0},
    {"sentence": "La forêt abrite de nombreuses espèces animales.", "annotated_sentence": "La forêt abrite de nombreuses espèces animales.", "label": 0},
    {"sentence": "La musique jazz a une grande influence sur de nombreux genres musicaux.", "annotated_sentence": "La musique jazz a une grande influence sur de nombreux genres musicaux.", "label": 0},
    {"sentence": "Les fleurs dans le jardin sont magnifiques au printemps.", "annotated_sentence": "Les fleurs dans le jardin sont magnifiques au printemps.", "label": 0},
    {"sentence": "Le café est une boisson appréciée le matin.", "annotated_sentence": "Le café est une boisson appréciée le matin.", "label": 0},
    {"sentence": "Le théâtre est une forme d'art captivante qui a traversé les siècles.", "annotated_sentence": "Le théâtre est une forme d'art captivante qui a traversé les siècles.", "label": 0},
    {"sentence": "La poésie touche les cœurs des lecteurs avec ses mots poignants.", "annotated_sentence": "La poésie touche les cœurs des lecteurs avec ses mots poignants.", "label": 0},
    {"sentence": "La cuisine chinoise est variée et délicieuse, avec une multitude de saveurs.", "annotated_sentence": "La cuisine chinoise est variée et délicieuse, avec une multitude de saveurs.", "label": 0},
    {"sentence": "Les écoles préparent les enfants pour l'avenir en leur fournissant des connaissances essentielles.", "annotated_sentence": "Les écoles préparent les enfants pour l'avenir en leur fournissant des connaissances essentielles.", "label": 0},
    {"sentence": "Le cinéma offre une évasion du quotidien en transportant les spectateurs dans des mondes imaginaires.", "annotated_sentence": "Le cinéma offre une évasion du quotidien en transportant les spectateurs dans des mondes imaginaires.", "label": 0},
    {"sentence": "Les forêts sont essentielles pour l'écosystème, fournissant un habitat à de nombreuses espèces.", "annotated_sentence": "Les forêts sont essentielles pour l'écosystème, fournissant un habitat à de nombreuses espèces.", "label": 0},
    {"sentence": "La danse est une forme d'expression artistique qui permet aux danseurs de s'exprimer librement.", "annotated_sentence": "La danse est une forme d'expression artistique qui permet aux danseurs de s'exprimer librement.", "label": 0},
    {"sentence": "Les rivières serpentent à travers le paysage, créant des écosystèmes riches en biodiversité.", "annotated_sentence": "Les rivières serpentent à travers le paysage, créant des écosystèmes riches en biodiversité.", "label": 0},
    {"sentence": "Le silence règne dans la bibliothèque, où les lecteurs se plongent dans des livres captivants.", "annotated_sentence": "Le silence règne dans la bibliothèque, où les lecteurs se plongent dans des livres captivants.", "label": 0},
    {"sentence": "Les étoiles filantes illuminent la nuit d'une lueur magique et éphémère.", "annotated_sentence": "Les étoiles filantes illuminent la nuit d'une lueur magique et éphémère.", "label": 0},
    {"sentence": "Le cinéma offre une évasion du quotidien en plongeant les spectateurs dans des aventures palpitantes.", "annotated_sentence": "Le cinéma offre une évasion du quotidien en plongeant les spectateurs dans des aventures palpitantes.", "label": 0},
    {"sentence": "Le théâtre est une forme d'art captivante qui transporte le public dans des mondes imaginaires.", "annotated_sentence": "Le théâtre est une forme d'art captivante qui transporte le public dans des mondes imaginaires.", "label": 0},
    {"sentence": "La poésie touche les cœurs des lecteurs avec ses vers remplis d'émotion et de sensibilité.", "annotated_sentence": "La poésie touche les cœurs des lecteurs avec ses vers remplis d'émotion et de sensibilité.", "label": 0},
    {"sentence": "Les rues étroites de Venise forment un labyrinthe mystérieux où les voyageurs se perdent souvent.", "annotated_sentence": "Les rues étroites de <ville>Venise</ville> forment un labyrinthe mystérieux où les voyageurs se perdent souvent.", "label": 1},
    {"sentence": "La gastronomie parisienne est célèbre pour ses plats exquis, comme le coq au vin et les escargots.", "annotated_sentence": "La gastronomie parisienne est célèbre pour ses plats exquis, comme le coq au vin et les escargots.", "label": 1},
    {"sentence": "Les gratte-ciels de New York s'élèvent vers le ciel, créant une impressionnante ligne d'horizon urbaine.", "annotated_sentence": "Les gratte-ciels de <ville>New York</ville> s'élèvent vers le ciel, créant une impressionnante ligne d'horizon urbaine.", "label": 1},
    {"sentence": "Les temples anciens d'Angkor Wat au Cambodge témoignent de la grandeur passée de cette cité antique.", "annotated_sentence": "Les temples anciens d'<ville>Angkor Wat</ville> au Cambodge témoignent de la grandeur passée de cette cité antique.", "label": 1},
    {"sentence": "Les rues animées de Tokyo sont remplies de néons lumineux et de stands de ramen.", "annotated_sentence": "Les rues animées de <ville>Tokyo</ville> sont remplies de néons lumineux et de stands de ramen.", "label": 1},
    {"sentence": "Les collines verdoyantes de la Toscane en Italie offrent des vues à couper le souffle sur les vignobles et les villages pittoresques.", "annotated_sentence": "Les collines verdoyantes de la Toscane en <ville>Italie</ville> offrent des vues à couper le souffle sur les vignobles et les villages pittoresques.", "label": 1},
    {"sentence": "Le désert de l'Arizona est un endroit aride et inhospitalier, mais les casinos de Las Vegas brillent comme des oasis dans cette étendue désertique.", "annotated_sentence": "Le désert de l'Arizona est un endroit aride et inhospitalier, mais les casinos de <ville>Las Vegas</ville> brillent comme des oasis dans cette étendue désertique.", "label": 1},
    {"sentence": "Les fjords norvégiens, comme le Geirangerfjord, sont des merveilles naturelles à couper le souffle.", "annotated_sentence": "Les fjords norvégiens, comme le <ville>Geirangerfjord</ville>, sont des merveilles naturelles à couper le souffle.", "label": 1},
    {"sentence": "Le quartier historique de La Havane à Cuba est un dédale de ruelles colorées et de musées fascinants.", "annotated_sentence": "Le quartier historique de <ville>La Havane</ville> à Cuba est un dédale de ruelles colorées et de musées fascinants.", "label": 1},
    {"sentence": "Les plages de sable fin de Cancún au Mexique sont bordées d'eaux cristallines et de stations balnéaires de luxe.", "annotated_sentence": "Les plages de sable fin de <ville>Cancún</ville> au Mexique sont bordées d'eaux cristallines et de stations balnéaires de luxe.", "label": 1},
    {"sentence": "La philosophie antique explore des questions fondamentales sur l'existence humaine et la nature de la réalité.", "annotated_sentence": "La philosophie antique explore des questions fondamentales sur l'existence humaine et la nature de la réalité.", "label": 0},
    {"sentence": "La musique classique apaise l'âme avec ses mélodies intemporelles et ses harmonies apaisantes.", "annotated_sentence": "La musique classique apaise l'âme avec ses mélodies intemporelles et ses harmonies apaisantes.", "label": 0},
    {"sentence": "La poésie transcende les frontières linguistiques pour communiquer des émotions universelles.", "annotated_sentence": "La poésie transcende les frontières linguistiques pour communiquer des émotions universelles.", "label": 0},
    {"sentence": "Les écoles préparent les enfants pour l'avenir en leur fournissant des connaissances essentielles.", "annotated_sentence": "Les écoles préparent les enfants pour l'avenir en leur fournissant des connaissances essentielles.", "label": 0},
    {"sentence": "Le silence règne dans la bibliothèque, où les lecteurs se plongent dans des livres captivants.", "annotated_sentence": "Le silence règne dans la bibliothèque, où les lecteurs se plongent dans des livres captivants.", "label": 0},
    {"sentence": "La danse est une forme d'expression artistique qui permet aux danseurs de s'exprimer librement.", "annotated_sentence": "La danse est une forme d'expression artistique qui permet aux danseurs de s'exprimer librement.", "label": 0},
    {"sentence": "Les étoiles filantes illuminent la nuit d'une lueur magique et éphémère.", "annotated_sentence": "Les étoiles filantes illuminent la nuit d'une lueur magique et éphémère.", "label": 0},
    {"sentence": "Le cinéma offre une évasion du quotidien en plongeant les spectateurs dans des aventures palpitantes.", "annotated_sentence": "Le cinéma offre une évasion du quotidien en plongeant les spectateurs dans des aventures palpitantes.", "label": 0},
    {"sentence": "Le théâtre est une forme d'art captivante qui transporte le public dans des mondes imaginaires.", "annotated_sentence": "Le théâtre est une forme d'art captivante qui transporte le public dans des mondes imaginaires.", "label": 0},
    {"sentence": "Les rivières serpentent à travers le paysage, créant des écosystèmes riches en biodiversité.", "annotated_sentence": "Les rivières serpentent à travers le paysage, créant des écosystèmes riches en biodiversité.", "label": 0},
    {"sentence": "Les canaux d'Amsterdam sont bordés de maisons étroites et colorées, créant une scène pittoresque.", "annotated_sentence": "Les canaux d'Amsterdam sont bordés de maisons étroites et colorées, créant une scène pittoresque.", "label": 1},
    {"sentence": "Les lumières scintillantes de Hong Kong illuminent la baie Victoria après le coucher du soleil.", "annotated_sentence": "Les lumières scintillantes de <ville>Hong Kong</ville> illuminent la baie Victoria après le coucher du soleil.", "label": 1},
    {"sentence": "Le château de Prague domine la vieille ville, rappelant l'histoire riche de la République tchèque.", "annotated_sentence": "Le château de <ville>Prague</ville> domine la vieille ville, rappelant l'histoire riche de la République tchèque.", "label": 1},
    {"sentence": "La Grande Muraille de Chine serpente à travers les montagnes, témoignant de la grandeur de l'ancienne civilisation chinoise.", "annotated_sentence": "La Grande Muraille de Chine serpente à travers les montagnes, témoignant de la grandeur de l'ancienne civilisation chinoise.", "label": 1},
    {"sentence": "Les plages de Rio de Janeiro sont célèbres dans le monde entier pour leur beauté naturelle et leur ambiance festive.", "annotated_sentence": "Les plages de <ville>Rio de Janeiro</ville> sont célèbres dans le monde entier pour leur beauté naturelle et leur ambiance festive.", "label": 1},
    {"sentence": "Les ruelles pavées de Florence sont remplies de sculptures de la Renaissance et de chefs-d'œuvre artistiques.", "annotated_sentence": "Les ruelles pavées de <ville>Florence</ville> sont remplies de sculptures de la Renaissance et de chefs-d'œuvre artistiques.", "label": 1},
    {"sentence": "La cathédrale de Cologne en Allemagne est un exemple stupéfiant de l'architecture gothique.", "annotated_sentence": "La cathédrale de <ville>Cologne</ville> en Allemagne est un exemple stupéfiant de l'architecture gothique.", "label": 1},
    {"sentence": "Les temples antiques d'Athènes témoignent de la riche histoire de la Grèce antique.", "annotated_sentence": "Les temples antiques d'<ville>Athènes</ville> témoignent de la riche histoire de la Grèce antique.", "label": 1},
    {"sentence": "La vieille ville de Jérusalem est un lieu saint pour trois grandes religions monothéistes.", "annotated_sentence": "La vieille ville de <ville>Jérusalem</ville> est un lieu saint pour trois grandes religions monothéistes.", "label": 1},
    {"sentence": "Les montagnes des Rocheuses offrent des aventures en plein air, de la randonnée à l'escalade.", "annotated_sentence": "Les montagnes des Rocheuses offrent des aventures en plein air, de la randonnée à l'escalade.", "label": 1},
    {"sentence": "La musique jazz a une grande influence sur la scène musicale moderne.", "annotated_sentence": "La musique jazz a une grande influence sur la scène musicale moderne.", "label": 0},
    {"sentence": "La philosophie explore des questions profondes sur la nature de la réalité et de la connaissance.", "annotated_sentence": "La philosophie explore des questions profondes sur la nature de la réalité et de la connaissance.", "label": 0},
    {"sentence": "La poésie transcende les barrières culturelles en exprimant des émotions universelles.", "annotated_sentence": "La poésie transcende les barrières culturelles en exprimant des émotions universelles.", "label": 0},
    {"sentence": "Le silence de la nuit est rompu par le chant des grillons et le murmure du vent.", "annotated_sentence": "Le silence de la nuit est rompu par le chant des grillons et le murmure du vent.", "label": 0},
    {"sentence": "La cuisine méditerranéenne est appréciée pour ses saveurs fraîches et ses ingrédients sains.", "annotated_sentence": "La cuisine méditerranéenne est appréciée pour ses saveurs fraîches et ses ingrédients sains.", "label": 0},
    {"sentence": "Les étoiles scintillent dans le ciel nocturne, évoquant des rêves et des espoirs.", "annotated_sentence": "Les étoiles scintillent dans le ciel nocturne, évoquant des rêves et des espoirs.", "label": 0},
    {"sentence": "La danse contemporaine défie les conventions et repousse les limites de l'expression corporelle.", "annotated_sentence": "La danse contemporaine défie les conventions et repousse les limites de l'expression corporelle.", "label": 0},
    {"sentence": "Le cinéma permet aux cinéastes de raconter des histoires captivantes à travers des images en mouvement.", "annotated_sentence": "Le cinéma permet aux cinéastes de raconter des histoires captivantes à travers des images en mouvement.", "label": 0},
    {"sentence": "Le théâtre classique grec a influencé de nombreuses formes de théâtre à travers les siècles.", "annotated_sentence": "Le théâtre classique grec a influencé de nombreuses formes de théâtre à travers les siècles.", "label": 0},
    {"sentence": "Les forêts tropicales abritent une incroyable diversité de plantes et d'animaux.", "annotated_sentence": "Les forêts tropicales abritent une incroyable diversité de plantes et d'animaux.", "label": 0},
    {"sentence": "Penses-tu que je puisse me rendre à Port-la-Nouvelle depuis Carcassonne", "annotated_sentence": "Penses-tu que je puisse me rendre à <ville>Port-la-Nouvelle</ville> depuis <ville>Carcassonne</ville>", "label": 1},
    {"sentence": "Le désert du Sahara s'étend sur plusieurs pays d'Afrique.", "annotated_sentence": "Le désert du Sahara s'étend sur plusieurs pays d'Afrique.", "label": 0}
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
for epoch in range(10):
    for batch in train_dataloader:
        optimizer.zero_grad()
        inputs, masks, labels = batch
        outputs = model(input_ids=inputs, attention_mask=masks, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        print(loss, outputs, inputs, masks, labels)

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
