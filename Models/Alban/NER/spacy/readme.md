# Installer spacy fr

python -m spacy download fr_core_news_sm

# Pour l'entrainement

Installer le fichier de configuration ici : https://spacy.io/usage/trainings

Activer les configs : python -m spacy init fill-config base_config.cfg config.cfg

Train le modèle dans le terminal : python3 -m spacy train ./config/config.cfg --output ./output/ --paths.train ./data/train.spacy --paths.dev ./data/val.spacy
