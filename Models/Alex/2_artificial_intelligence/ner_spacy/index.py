import spacy
from pathlib import Path


def load_model(model_path):

    return spacy.load(model_path)


def get_entities(nlp, text):

    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]


def main(model_path):

    print("[SERVER] -> Starting : Loading artificial intelligence...")

    nlp = load_model(model_path)

    print("[SERVER] -> Starting : Artificial intelligence loaded.")
    print("[SERVER] -> Starting : Starting process ended in FR language. Waiting for user input")

    while True:

        text = input(
            "$[SERVER] -> LOG : Quel est votre itinéraire ? (ou tapez 'e' pour quitter) : ")

        if text.lower() == 'e':
            print("[SERVER] -> END PROCESS : Server shutdown.")
            break

        entities = get_entities(nlp, text)
        if entities:
            print("[SERVER] -> ANALYSIS RESULT : Entités trouvées et leurs labels :")
            for ent_text, ent_label in entities:
                print(f" - {ent_label} : {ent_text} ")
        else:
            print("[SERVER] -> ANALYSIS RESULT : Aucune entité trouvée.")

        print("\n")


if __name__ == "__main__":

    current_dir = Path(__file__).parent
    model_dir = current_dir / "model_output"
    main(str(model_dir))
