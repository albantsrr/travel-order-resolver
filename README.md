# Générateur de Données - README

Ce script Python est un générateur de phrases qui vous permet de créer des jeux de données adaptés au projet T-AIA-901. Il prend en charge diverses options pour personnaliser la génération de données en fonction de vos besoins.

## Configuration Requise
- Python : 3.10.11

## Utilisation

Pour exécuter le script, utilisez la commande suivante :
python generation.py [-h] [--csv CSV] [--name NAME] [--gen GEN] [--nb NB]

### Options

- `-h`, `--help` : Affiche ce message d'aide et quitte le script.

- `--csv CSV` : Active ou désactive la génération de fichiers CSV. Utilisez 0 pour désactiver et 1 pour activer.

- `--name NAME` : Spécifiez le nom du fichier CSV résultant.

- `--gen GEN` : Choisissez le type de génération souhaité :
  - 0 : Toutes les phrases
  - 1 : Phrase 1
  - 2 : Phrase 2
  - 3 : Phrase 3

- `--nb NB` : Définissez le nombre de phrases à générer.

## Exemple d'Utilisation

Pour générer un fichier CSV avec 300 phrases, vous pouvez utiliser la commande suivante (dans un environnement Windows) :

python generation.py --csv 1 --name dataSet --gen 0 --nb 300
