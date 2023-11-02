from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException


import random
import csv
import os
import re

GLB_INVALID_LINK = ["modifier", "modifier le code", "Modifier le code",
                     "Voir l’historique", "archive", "Politique de confidentialité",
                     "À propos de Wikipédia", "Avertissements", "Contact" , "Code de conduite",
                     "Statistiques" , "Développeurs", "Déclaration sur les témoins (cookies)",
                     "Version mobile", "licence Creative Commons attribution, partage dans les mêmes conditions",
                     "Wikimedia Foundation, Inc.", "Voir le texte source", "Poser une question", "Sommaire de l'aide",
                     "Portails thématiques", "Principes fondateurs", "Accueil de la communauté", "Comment contribuer ?",
                     "conditions d’utilisation", "Créer un compte", "Discussion", "vérifiabilité", "Se connecter",
                     "poser une question", "Catégories", "[réf. nécessaire]", "Votre aide", "archive", "Recherche interne"
                     "votre page d'accueil"
                    ]

GLB_INVALID_WORD_IN_LINK = ["Aide", "Utilisateur", "Wikipédia", "Arborescence", "Catégorie", "Spéciale", "Portail", "Plan", "Projet"]

GLB_SPECIFICS_WORDS = []
# GLB_SPECIFICS_WORDS = ["depuis", "Depuis"]

class cScrapper:
    def __init__(self):
        self.path = r"https://fr.wikipedia.org/wiki/Contrefa%C3%A7on_horlog%C3%A8re"
        self.path_csv = r"random_french_sentences.csv"

        self.number = 0

        self.list_sentence = []
        self.list_csv_row = []

        self.list_links = []

        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True
        chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.path)


    def __add_csv_row(self, sentence):
        csv_row = []
        #ID
        csv_row.append("")
        #SENTENCE
        csv_row.append(sentence)
        #VALID
        csv_row.append(0)
        #ORIGIN
        csv_row.append("")
        #ARRIVAL
        csv_row.append("")
        #STEP_OVER
        csv_row.append("")
        #TYPE
        csv_row.append("")

        self.list_csv_row.append(csv_row)

    def __add_sentence(self, list_paragraph):
        if(len(GLB_SPECIFICS_WORDS) > 0):
            self.__add_sentence_from_specific_word(list_paragraph)
        else:
            self.__add_sentence_without_specific_word(list_paragraph)
        
    def __add_sentence_from_specific_word(self, list_paragraph):

        for i in range(len(list_paragraph)):
                paragraph = list_paragraph[i]

                for i in range(len(GLB_SPECIFICS_WORDS)):
                    specific_word = GLB_SPECIFICS_WORDS[i]
                
                    if(specific_word in paragraph.text ):
                        sentences = paragraph.text.split(".")
                
                        for j in range(len(sentences)):
                            sentence = sentences[j]
                
                            if(specific_word in sentence):    
                                if(self.__is_Valid_Sentence(sentence)):
                                    sentence = sentence + "." 
                                    if sentence.startswith(' '):
                                        sentence = sentence.lstrip()
                                    if(not (sentence in self.list_sentence)):
                                        sentence = sentence.replace("\n", "") 
                                        self.list_sentence.append(sentence)
                                        self.__add_csv_row(sentence)

    def __add_sentence_without_specific_word(self, list_paragraph):
        for i in range(len(list_paragraph)):
                paragraph = list_paragraph[i]
                sentences = paragraph.text.split(".")

                for j in range(len(sentences)):
                    sentence = sentences[j]    

                    if(self.__is_Valid_Sentence(sentence)):
                        sentence = sentence + "." 
                        if sentence.startswith(' '):
                            sentence = sentence.lstrip()
                        if(not (sentence in self.list_sentence)):
                            sentence = sentence.replace("\n", "") 
                            self.list_sentence.append(sentence)
                            self.__add_csv_row(sentence)


    def __is_Valid_Link(self, link):
        if(len(link.text) < 10):
            return False
        
        href_value = link.get_attribute("href")
        if href_value:
            if (not href_value.startswith('https://fr.wikipedia.org/')):
                return False

        if(link.text in GLB_INVALID_LINK):
            return False
        
        if re.search(r'[{}"]', link.text):
            return False

        class_value = link.get_attribute("class")
        if(class_value):
            return False
        
        title_value = link.get_attribute("title")
        if(title_value):
            for i in range(len(GLB_INVALID_WORD_IN_LINK)):
                word = GLB_INVALID_WORD_IN_LINK[i]

                if(word in title_value):
                    return False

        return True

    def __is_Valid_Sentence(self, sentence):
        if(len(sentence) < 15):
            return False
                
        if re.search(r'[\@\#\$\%\^\&\*\(\)\_\+\{\}\[\]\:\,\;\<\>\~\\\/\|\=\«\»\.\•\-]', sentence):
            return False
        
        return True


    def __get_Indice_Link(self,size):
        start_rand = 0
        end_rand =  size-1

        return random.randint(start_rand, end_rand)

    def __get_link(self, list_link):
        for i in range(len(list_link)):
                indice_link = self.__get_Indice_Link(len(list_link))
                link = list_link[indice_link]

                if(self.__is_Valid_Link(link)):
                    return link

        return -1 


    def start(self, number):
        if(number <= 0):
            return 
               
        try:
            # sleep(1)
            window_handles = self.driver.window_handles

            new_window_handle = window_handles[-1]

            self.driver.switch_to.window(new_window_handle)

            list_paragraph = self.driver.find_elements(By.TAG_NAME, "p")
            list_link = self.driver.find_elements(By.TAG_NAME, 'a')

            link = self.__get_link(list_link)
            if(link == -1):
                print(f"no valid link found")
                return

            count = len(self.list_sentence)
            self.__add_sentence(list_paragraph)

            print(f"size liste of sentences : {len(self.list_sentence)}")
            print(f"next link to click : {link.text}")
            print()

            link.click()

            new_number = number - (len(self.list_sentence) - count )  
            self.start(new_number)

        except Exception as e:
            print(f"<Error> : {str(e)}")
            print("error")
            # self.driver.close()
            return

    def write_csv(self):
        if not os.path.isfile(self.path_csv):
            with open(self.path_csv, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile,delimiter=';')
                csv_writer.writerow(['ID','SENTENCE','VALID','ORIGIN','ARRIVAL','STEP_OVER','TYPE'])
            
        with open(self.path_csv, 'a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile,delimiter=';')
            
            for i in range(len(self.list_csv_row)):
                    row = self.list_csv_row[i]
                    row[0] = i
                    csv_writer.writerow(row)



if __name__ == "__main__":
    c_scrapper = cScrapper()
    c_scrapper.start(10000)
    c_scrapper.write_csv()
