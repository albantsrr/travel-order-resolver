import logging
import time
logging.basicConfig(
    filename=r'logs\distilbert.log',
    filemode='w', 
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

start = time.time()
import pandas as pd
import random
from sklearn.model_selection import train_test_split
from transformers import DistilBertTokenizer 
from transformers import DistilBertForSequenceClassification
from transformers import Trainer, TrainingArguments
import torch
end = time.time()
logging.debug(f"<TIME> load library :  {end-start}")


class cDataSet:
    def __init__(self):
        self.list_path = [r"dataset\random_french_sentences.csv", r"dataset\generate_sentence.csv", r"dataset\sentences.json"]

        self.list_sentences = []
        self.list_labels = []

        self.train_sentences = []
        self.test_sentences = []
        self.val_sentences = []

        self.train_labels = []
        self.test_labels = []
        self.val_labels = []

    def read_file(self):
        start = time.time()
        # random_phrase.csv 
        path = self.list_path[0]
        dataframef_1 = pd.read_csv(path, delimiter=';') 
        list_sentence_1 = dataframef_1["SENTENCE"].tolist()
        list_labels_1 = dataframef_1["VALID"].tolist()

        #sentence_generation.csv
        path = self.list_path[1]
        dataframef_2 = pd.read_csv(path, delimiter=';') 
        list_sentence_2 = dataframef_2["SENTENCE"].tolist()
        list_labels_2 = dataframef_2["VALID"].tolist()

        #sentences.json
        path = self.list_path[2]
        dataframef_3 = pd.read_json(path) 
        list_sentence_3 = dataframef_3["sentence"].tolist()
        list_labels_3 = dataframef_3["label"].tolist()

        self.list_sentences = list_sentence_1 + list_sentence_2 + list_sentence_3
        self.list_labels = list_labels_1 + list_labels_2 + list_labels_3 
        end = time.time()
        logging.debug(f"<TIME> load dataset :  {end-start}")
        
        ###############################################################
        #  sous echantillon
        combined_data = list(zip(self.list_sentences, self.list_labels))

        random.shuffle(combined_data)

        self.list_sentences, self.list_labels = zip(*combined_data)
        self.list_sentences = list(self.list_sentences)
        self.list_labels = list(self.list_labels)

        self.list_sentences = self.list_sentences[0:30000]
        self.list_labels = self.list_labels[0:30000]
        ###############################################################

        number_of_invalid = 0
        number_of_valid = 0
        for label in self.list_labels:
            if(label == 0):
                number_of_invalid += 1
            elif(label == 1):
                number_of_valid += 1

        logging.info(f"number of valid sentences : {number_of_valid}")
        logging.info(f"number of invalid sentences : {number_of_invalid}")
        logging.info(f"<distilbert:cDataSet:read_file> size list of sentences : {len(self.list_sentences)}")    

    def split_sentences(self):
        start = time.time()
        self.train_sentences, self.test_sentences, self.train_labels, self.test_labels = train_test_split(self.list_sentences, self.list_labels, test_size=0.2, random_state=42)
        self.train_sentences, self.val_sentences, self.train_labels, self.val_labels = train_test_split(self.train_sentences, self.train_labels, test_size=0.2, random_state=42)
        end = time.time()

        logging.debug(f"<TIME> split dataset :  {end-start}")
        logging.info(f"<distilbert:cDataSet:split_sentences> size of train dataset : {len(self.train_sentences)}") 
        logging.info(f"<distilbert:cDataSet:split_sentences> size of test dataset : {len(self.test_sentences)}") 
        logging.info(f"<distilbert:cDataSet:split_sentences> size of val dataset : {len(self.val_sentences)}") 


class CityDataset(torch.utils.data.Dataset):
    
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item
    
    def __len__(self):
        return len(self.labels)

class cModel:
    def __init__(self):
        self.dataset = cDataSet()
        self.tokenizer= None

        self.train_encodings = None
        self.test_encodings = None
        self.val_encodings = None

        self.train_dataset = None
        self.val_dataset = None 
        self.test_dataset = None 

        self.model = None

        self.training_args = None
        self.trainer = None

    def set_up(self):
        self.dataset.read_file()
        self.dataset.split_sentences()

        start = time.time()
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        end = time.time()
        logging.debug(f"<TIME> load tokenizer distilbert-base-uncased :  {end-start}")

        start = time.time()
        self.train_encodings = self.tokenizer(self.dataset.train_sentences, truncation=True, padding=True, max_length=128, return_tensors="pt")
        self.test_encodings = self.tokenizer(self.dataset.test_sentences, truncation=True, padding=True, max_length=128, return_tensors="pt")
        self.val_encodings = self.tokenizer(self.dataset.val_sentences, truncation=True, padding=True, max_length=128, return_tensors="pt")
        end = time.time()
        logging.debug(f"<TIME> tokenize dataset :  {end-start}")

        start = time.time()
        self.train_dataset = CityDataset(self.train_encodings, self.dataset.train_labels)
        self.val_dataset = CityDataset(self.val_encodings, self.dataset.val_labels)
        self.test_dataset = CityDataset(self.test_encodings, self.dataset.test_labels)
        end = time.time()
        logging.debug(f"<TIME> create dataset with CityDataset  :  {end-start}")

        start = time.time()
        self.model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=2)
        end = time.time()
        logging.debug(f"<TIME> load distilbert-base-uncased model :  {end-start}")
        
    def set_up_training(self):
        num_epochs = 6
        batch_size = 64 

        self.training_args = TrainingArguments(
            per_device_train_batch_size=batch_size,
            num_train_epochs=num_epochs,
            logging_dir='./logs',
            logging_steps=10,
            evaluation_strategy="epoch",
            output_dir='./results',
            save_total_limit=2
        )

        self.trainer = Trainer(
            model=self.model,
            args=self.training_args,
            train_dataset=self.train_dataset,
            eval_dataset=self.val_dataset
        )

    def train_model(self):
        self.trainer.train()
        test_results = self.trainer.evaluate(self.test_dataset)

        self.trainer.save_model("model/disitilbert_model_30000")
        self.tokenizer.save_pretrained(r"model/disitilbert_tokenizer_30000")

    def try_it(self):
        while(1):
            print("phrase :")
            input_text = str(input())

            if(input_text == "STOP"):
                break

            test_encoding = self.tokenizer([input_text], truncation=True, padding=True, max_length=128, return_tensors="pt")
            test_dataset_single = CityDataset(test_encoding, [0])
            prediction = self.trainer.predict(test_dataset_single)
            predicted_label = prediction.predictions.argmax(axis=1)[0] 
            print(prediction.predictions.argmax(axis=1))
            if predicted_label == 1:
                print("La phrase contient un itinéraire")
            else:
                print("La phrase ne contient pas d'itinéraire")


test = cModel()
test.set_up()
test.set_up_training()
test.train_model()
test.try_it()