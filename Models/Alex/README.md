# Voice to text + Dataset Generation + NER

## Voice to text

![image](https://github.com/EpitechMscProPromo2024/T-AIA-901-TLS_2/assets/53010854/cac2df9c-70ab-434d-8bd5-7c27725e1148)


### Start vocie to text server : 

- Go to the `voice_to_text` folder. The root of this folder is the `app-server` folder where you can find the `server.js` file witch threat the voice audio and communicate with google APIS from transform them from voice to text..
- Run the `npm install` command for installing voice to text server dependencies.
- Node run `server.js` for starting the voice to text server.

### Start Next JS client front-end dashboard : 

- Go to the `app-client` folder. It's the front-end dashboard of the application in NEXT JS. Even if you can have a SSR mode, assume that it is just a simple client server. 
- Run the `npm install` command
- Run the `npm run dev` command for starting the front-end dashboard.

------------

## Dataset Generation

- Go to the `dataset_generation_ner_spacy` folder
- Go to `generators/gen` folder
- For generating the datasets (train, test, validation), execute the `main.py` file with the following command: `python3 main.py`
- Then verify the generated datasets with `python3 verification.py`
- You can then read the generated datasets with in the `dataset` folder

- If you are okay with the generated datasets, move them to their respective folders in the `ner_spacy/dataset` folder at the root folder of the project.
  
------------

## NER Spacy 

### Training

- Go to the `ner_spacy` folder
- Run the `ner_training.py` file with the following command: `python3 main.py`


Conseils nico : 
optimizer, loss function, les hyperparamètres à check
