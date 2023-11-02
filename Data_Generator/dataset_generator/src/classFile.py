# classFile.py
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Confidential file
# Copyright (C) Epitech - All rights reserved
# -----------------------------------------------------------------------------
#
#  
#
# -----------------------------------------------------------------------------
# History
# 03/10/2023 N. Laurens : creation
# 14/10/2023 N. Laurens : Use timetable.csv instead of stops.txt
# 21/10/2023 N. Laurens : add cGenration_1_Valid & cGenration_1_Invalid
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Import
# -----------------------------------------------------------------------------
import csv
import random
import os

class cStops:
    def __init__(self):
        self.path = r"res\stops.txt"
        self.data = []

        self.list_trainStationName = []
        self.list_trainStationLocation = []

        self.setUp()

    def setUp(self):
        self.readTxt()
        self.formatData()

    def formatData(self):
        for i in range(len(self.data)):
            elem = self.data[i]
            name = elem[1].strip('"')
            lat = elem[3]
            long = elem[4]
            if(lat == "" or long == "" ):
                print("line = ", (i+2))
            else:
                pos = [float(lat),float(long)]
            
                if(name not in self.list_trainStationName):
                    self.list_trainStationName.append(name)
                    self.list_trainStationLocation.append(pos)

    def getPos(self,listName):
        listPos = []
        for i in range(len(listName)):
            name = listName[i]
            pos = [0,0]
            if(name in self.list_trainStationName):
                index = self.list_trainStationName.index(name)
                pos = self.list_trainStationLocation[index]
            listPos.append(pos)
        
        return listPos            


    def readTxt(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            rows = file.readlines() 
            
        for i in range(len(rows)-1):
            row = rows[i+1]
            t_listData = row.split(',')
            self.data.append(t_listData)

    def toString(self):
        print("size list_trainStationName",len(self.list_trainStationName))
        print("size list_trainStationLocation",len(self.list_trainStationLocation))

class cTimeTables:
    def __init__(self):
        self.path = r"res\timetables.csv"
        self.data = []

        self.list_trainStationName = []
        self.list_formated_name = []

    def setUp(self):
        self.__read_csv()
        self.__format_data()

    def __format_data(self):
        for i in range(len(self.data)):
            elem = self.data[i]
            names = elem[1]
            list_name = names.split(" - ")
            if(len(list_name)> 2):
                print(list_name)
                continue
            if(not list_name[0] in self.list_trainStationName):
                self.list_trainStationName.append(list_name[0])
                formated_name = self.__format_name(list_name[0])
                self.list_formated_name.append(formated_name)
            if(not list_name[1] in self.list_trainStationName):
                self.list_trainStationName.append(list_name[1])
                formated_name = self.__format_name(list_name[1])
                self.list_formated_name.append(formated_name)

    def __format_name(self,name):
        formated_name = name
        if("Gare de " in name):
            list_name = name.split("Gare de ")
            formated_name = list_name[1] 
        return formated_name

    def __read_csv(self):
        # self.path=r"..\res\timetables.csv"
        with open(self.path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            i = 0
            for row in csv_reader:
                if(i == 0):
                    i+=1
                    continue

                t_listData = row[0].split('\t')
                self.data.append(t_listData)

    def toString(self):
        print(f"size list_trainStationName : {len(self.list_trainStationName)}")
        print(f"size list_formated_name : {len(self.list_formated_name)}")

class cListDesGares:
    def __init__(self):
        self.path =r"res\liste-des-gares.csv"

        self.data = []

        self.list_id = []
        self.list_libelle = []
        self.list_commune = []
        self.list_departement = []

    def setUp(self):
        self.__read_csv()
        self.__format_data()

    def __format_data(self):
        for i in range(len(self.data)):
            elem = self.data[i]
            self.list_id.append(elem[0])
            self.list_libelle.append(elem[1])
            commune = elem[7]
            if(not commune in self.list_commune):
                self.list_commune.append(commune)
            departement = elem[8]
            if(not departement in self.list_departement):
                self.list_departement.append(departement)


    def __read_csv(self):
        # self.path = r"..\res\liste-des-gares.csv"
        with open(self.path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            i = 0
            for row in csv_reader:
                if(i == 0):
                    i+=1
                    continue

                self.data.append(row[0].split(";"))



class cGeneration_1_Invalid:
    def __init__(self):
        self.path = r"res/generation_1_invalide.txt"
        
        self.list_sentence = []
        self.list_csv_row = []

        self.list_name_city = []
        self.list_name_trainStation = []

        self.list_verbe = []
        self.list_intention_visiter = []
        self.list_intention_activite = []
        self.list_activite = []

    def _add_csv_row(self, sentence):
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
        
    def read_File(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            rows = file.readlines()
            step = 0

            for i in range(len(rows)):
                row = rows[i]
                listText = row.split("\n")
                text = listText[0]
                if(text == "[Verbe]"):
                    step = 1
                    continue

                if(text == "[Intention Visiter]"):
                    step = 2
                    continue

                if(text == "[Intention Activite]"):
                    step = 3
                    continue

                if(text == "[Activite]"):
                    step = 4
                    continue

                if(text == "END"):
                    step = 0
                    continue

                if(text != ""):
                    match step:
                        case 1:
                            self.list_verbe.append(text)
                            continue
                        case 2:
                            self.list_intention_visiter.append(text)
                            continue
                        case 3:
                            self.list_intention_activite.append(text)
                            continue
                        case 4:
                            self.list_activite.append(text)
                            continue
                        case _:
                            continue

    def generate_by_number(self, number):
        for i in range(number):
            sentence = ""

            index_verbe = random.randrange(len(self.list_verbe))
            verbe = self.list_verbe[index_verbe]
 
            type_intention = random.randint(1, 2)

            invalid_text = self.__get_invalid_text(type_intention)

            sentence = verbe + " " + invalid_text

            self.list_sentence.append(sentence)
            self._add_csv_row(sentence)
            

    def __generate_intention_activite(self):
        sentence = ""

        index_intention_activite = random.randrange(len(self.list_intention_activite))
        intention_activite = self.list_intention_activite[index_intention_activite]

        index_activite = random.randrange(len(self.list_activite))
        activite = self.list_activite[index_activite]

        sentence = intention_activite + " " + activite
        return  sentence
    
    def __generate_intention_visiter(self):
        sentence = ""
        intention_visiter = ""
        city = ""

        if(len(self.list_intention_visiter) > 0):
            index_intention_visiter = random.randrange(len(self.list_intention_visiter))
            intention_visiter = self.list_intention_visiter[index_intention_visiter]

        if(len(self.list_name_city)):
            index_city = random.randrange(len(self.list_name_city))
            city = self.list_name_city[index_city]

        sentence = intention_visiter + " " + city
        return  sentence


    def __get_invalid_text(self, intention):
        match intention:
            case 1 : 
                return self.__generate_intention_activite()
            case 2 :
                return self.__generate_intention_visiter()
            case _:
                return ""


    def set_List_Name_City(self, arg_list_name_city):
        self.list_name_city = arg_list_name_city

    def set_List_Name_TrainStation(self, arg_list_name_trainStation):
        self.list_name_trainStation = arg_list_name_trainStation

class cGeneration_1_Valid:
    def __init__(self):
        self.path = r"res/generation_1_valide.txt"
        
        self.list_sentence = []
        self.list_csv_row = []

        self.list_name_city = []
        self.list_name_trainStation = []

        self.list_verbe = []
        self.list_intention = []
        self.list_mot_start = []
        self.list_mot_end = []

        #
        self.propotion_city = 100

    def _add_csv_row(self, sentence):
        csv_row = []
        #ID
        csv_row.append("")
        #SENTENCE
        csv_row.append(sentence)
        #VALID
        csv_row.append(1)
        #ORIGIN
        csv_row.append("")
        #ARRIVAL
        csv_row.append("")
        #STEP_OVER
        csv_row.append("")
        #TYPE
        csv_row.append("")

        self.list_csv_row.append(csv_row)

    def read_File(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            rows = file.readlines()
            step = 0

            for i in range(len(rows)):
                row = rows[i]
                listText = row.split("\n")
                text = listText[0]
                if(text == "[Verbe]"):
                    step = 1
                    continue

                if(text == "[Intention Valide]"):
                    step = 2
                    continue

                if(text == "[Mot Start]"):
                    step = 3
                    continue

                if(text == "[Mot End]"):
                    step = 4
                    continue

                if(text == "END"):
                    step = 0
                    continue

                if(text != ""):
                    match step:
                        case 1:
                            self.list_verbe.append(text)
                            continue
                        case 2:
                            self.list_intention.append(text)
                            continue
                        case 3:
                            self.list_mot_start.append(text)
                            continue
                        case 4:
                            self.list_mot_end.append(text)
                            continue
                        case _:
                            continue

    def generate_by_number(self, number):
        number_sentence_city = int((number*self.propotion_city)/100)
        for i in range(number):
            sentence = ""
            verbe = "je veux"
            intention = "aller"
            mot_start = "de"
            location_start = "TOULOUSE"
            mot_start = "à"
            location_end= "PARIS"

            if(len(self.list_verbe) > 0):
                index_verbe = random.randrange(len(self.list_verbe))
                verbe = self.list_verbe[index_verbe]
 
            if(len(self.list_intention) > 0):
                index_intention = random.randrange(len(self.list_intention))
                intention = self.list_intention[index_intention]

            if(len(self.list_mot_start) > 0):
                index_mot_start = random.randrange(len(self.list_mot_start))
                mot_start = self.list_mot_start[index_mot_start]

            if(len(self.list_mot_end) > 0):
                index_mot_end = random.randrange(len(self.list_mot_end))
                mot_end = self.list_mot_end[index_mot_end]

            if(i <= number_sentence_city):
                if(len(self.list_name_city) > 0):
                    index_location_start = random.randrange(len(self.list_name_city))
                    location_start = self.list_name_city[index_location_start]

                    index_location_end = random.randrange(len(self.list_name_city))
                    location_end = self.list_name_city[index_location_end]
            else:
                if(len(self.list_name_trainStation) > 0):
                    index_location_start = random.randrange(len(self.list_name_trainStation))
                    location_start = self.list_name_city[index_location_start]

                    index_location_end = random.randrange(len(self.list_name_trainStation))
                    location_end = self.list_name_city[index_location_end]

            if(i <= (int(number/2))):
                sentence = verbe + " " + intention + " " + mot_start + " " + location_start + " " + mot_end + " " + location_end  
            else:
                sentence = verbe + " " + intention + " " + mot_end + " " + location_end + " " +  mot_start + " " + location_start

            self.list_sentence.append(sentence)
            self._add_csv_row(sentence)

    def set_List_Name_City(self, arg_list_name_city):
        self.list_name_city = arg_list_name_city

    def set_List_Name_TrainStation(self, arg_list_name_trainStation):
        self.list_name_trainStation = arg_list_name_trainStation


class cGeneration_2_Invalid:
    def __init__(self):
        self.path = r"res/generation_2_invalide.txt"
        
        self.list_sentence = []
        self.list_csv_row = []

        self.list_name_city = []
        self.list_name_trainStation = []

        self.list_mot_interrogatif = []
        self.list_optionnel = []
        self.list_verbe = []
        self.list_intention_voyage = []
        self.list_transport = []
        self.list_activite = []

    def _add_csv_row(self, sentence):
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


    def __generate_intention_activite(self):
        sentence = ""
        activite = "un dîner"

        index_activite = random.randrange(len(self.list_activite))
        activite = self.list_activite[index_activite]

        sentence = activite
        return  sentence
    
    def __generate_intention_voyage(self):
        sentence = ""
        intention_voyage = "un déplacement"
        transport = "en voiture" 
        city = "à TOULOUSE"

        if(len(self.list_transport) > 0):
            index_transport = random.randrange(len(self.list_transport))
            transport ="en " +  self.list_transport[index_transport]

        if(len(self.list_intention_voyage) > 0):
            index_intention_voyage = random.randrange(len(self.list_intention_voyage))
            intention_voyage = self.list_intention_voyage[index_intention_voyage]

        if(len(self.list_name_city)):
            index_city = random.randrange(len(self.list_name_city))
            city = "à " + self.list_name_city[index_city]

        type_intention = random.randint(1, 2)

        if(type_intention == 1):
            sentence = intention_voyage + " " + city + " " + transport

        elif(type_intention == 2):
            sentence = intention_voyage + " " + city

        return  sentence

    def __get_invalid_text(self, intention):
        match intention:
            case 1 : 
                return self.__generate_intention_activite()
            case 2 :
                return self.__generate_intention_voyage()
            case _:
                return ""


    def generate_by_number(self, number):
        for i in range(number):
            sentence = ""
            mot_iterrogatif = "de quelle manière"
            optionnel = ""
            verbe = "faire"
            invalid_text = "un voyage à PARIS en avion"

            if(len(self.list_mot_interrogatif) > 0):
                index_mot_interrogatif = random.randrange(len(self.list_mot_interrogatif))
                mot_iterrogatif = self.list_mot_interrogatif[index_mot_interrogatif]

            if(len(self.list_optionnel) > 0):
                optionnel_active = random.randint(0,1)
                if(optionnel_active):
                    index_optionnel = random.randrange(len(self.list_optionnel))
                    optionnel = " " + self.list_optionnel[index_optionnel]

            if(len(self.list_verbe) > 0):
                index_verbe = random.randrange(len(self.list_verbe))
                verbe = self.list_verbe[index_verbe]

            type_intention = random.randint(1, 2)

            invalid_text = self.__get_invalid_text(type_intention)

            sentence = mot_iterrogatif + optionnel + " " + verbe + " " + invalid_text

            self.list_sentence.append(sentence)
            self._add_csv_row(sentence)

    def read_File(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            rows = file.readlines()
            step = 0

            for i in range(len(rows)):
                row = rows[i]
                listText = row.split("\n")
                text = listText[0]
                if(text == "[Mot interrogatif]"):
                    step = 1
                    continue

                if(text == "[Optionnel]"):
                    step = 2
                    continue

                if(text == "[Verbe]"):
                    step = 3
                    continue

                if(text == "[Intention Voyage]"):
                    step = 4
                    continue

                if(text == "[Transport]"):
                    step = 5
                    continue

                if(text == "[Activite]"):
                    step = 6
                    continue

                if(text == "END"):
                    step = 0
                    continue

                if(text != ""):
                    match step:
                        case 1:
                            self.list_mot_interrogatif.append(text)
                            continue
                        case 2:
                            self.list_optionnel.append(text)
                            continue
                        case 3:
                            self.list_verbe.append(text)
                            continue
                        case 4:
                            self.list_intention_voyage.append(text)
                            continue
                        case 5:
                            self.list_transport.append(text)
                            continue
                        case 6:
                            self.list_activite.append(text)
                            continue
                        case _:
                            continue
            
    def set_List_Name_City(self, arg_list_name_city):
        self.list_name_city = arg_list_name_city

    def set_List_Name_TrainStation(self, arg_list_name_trainStation):
        self.list_name_trainStation = arg_list_name_trainStation

class cGeneration_2_Valid:
    def __init__(self):
        self.path = r"res/generation_2_valide.txt"
        
        self.list_sentence = []
        self.list_csv_row = []

        self.list_name_city = []
        self.list_name_trainStation = []

        self.list_mot_interrogatif = []
        self.list_optionnel = []
        self.list_verbe = []
        self.list_intention = []

        #
        self.propotion_city = 100

    def _add_csv_row(self, sentence):
        csv_row = []
        #ID
        csv_row.append("")
        #SENTENCE
        csv_row.append(sentence)
        #VALID
        csv_row.append(1)
        #ORIGIN
        csv_row.append("")
        #ARRIVAL
        csv_row.append("")
        #STEP_OVER
        csv_row.append("")
        #TYPE
        csv_row.append("")

        self.list_csv_row.append(csv_row)

    def read_File(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            rows = file.readlines()
            step = 0

            for i in range(len(rows)):
                row = rows[i]
                listText = row.split("\n")
                text = listText[0]
                if(text == "[Mot interrogatif]"):
                    step = 1
                    continue

                if(text == "[Optionnel]"):
                    step = 2
                    continue

                if(text == "[Verbe]"):
                    step = 3
                    continue

                if(text == "[Intention Valide]"):
                    step = 4
                    continue

                if(text == "END"):
                    step = 0
                    continue

                if(text != ""):
                    match step:
                        case 1:
                            self.list_mot_interrogatif.append(text)
                            continue
                        case 2:
                            self.list_optionnel.append(text)
                            continue
                        case 3:
                            self.list_verbe.append(text)
                            continue
                        case 4:
                            self.list_intention.append(text)
                            continue
                        case _:
                            continue

    def generate_by_number(self, number):
        number_sentence_city = int((number*self.propotion_city)/100)
        for i in range(number):
            sentence = ""
            mot_iterrogatif = "de quelle manière"
            optionnel = ""
            verbe = "faire"
            intention = "le trajet"
            location_start = "TOULOUSE"
            location_end= "PARIS"

            if(len(self.list_mot_interrogatif) > 0):
                index_mot_interrogatif = random.randrange(len(self.list_mot_interrogatif))
                mot_iterrogatif = self.list_mot_interrogatif[index_mot_interrogatif]

            if(len(self.list_verbe) > 0):
                index_verbe = random.randrange(len(self.list_verbe))
                verbe = self.list_verbe[index_verbe]
 
            if(len(self.list_intention) > 0):
                index_intention = random.randrange(len(self.list_intention))
                intention = self.list_intention[index_intention]

            if(len(self.list_optionnel) > 0):
                optionnel_active = random.randint(0,1)
                if(optionnel_active):
                    index_optionnel = random.randrange(len(self.list_optionnel))
                    optionnel = " " + self.list_optionnel[index_optionnel]

            if(i <= number_sentence_city):
                if(len(self.list_name_city) > 0):
                    index_location_start = random.randrange(len(self.list_name_city))
                    location_start = self.list_name_city[index_location_start]

                    index_location_end = random.randrange(len(self.list_name_city))
                    location_end = self.list_name_city[index_location_end]
            else:
                if(len(self.list_name_trainStation) > 0):
                    index_location_start = random.randrange(len(self.list_name_trainStation))
                    location_start = self.list_name_city[index_location_start]

                    index_location_end = random.randrange(len(self.list_name_trainStation))
                    location_end = self.list_name_city[index_location_end]

            if(i <= (int(number/2))):
                sentence = mot_iterrogatif + optionnel + " " + verbe + " " + intention + " de " + location_start + " à " + location_end  
            else:
                sentence = mot_iterrogatif + optionnel + " " + verbe + " " + intention + " allant de " + location_start + " depuis " + location_end

            self.list_sentence.append(sentence)
            self._add_csv_row(sentence)

    def set_List_Name_City(self, arg_list_name_city):
        self.list_name_city = arg_list_name_city

    def set_List_Name_TrainStation(self, arg_list_name_trainStation):
        self.list_name_trainStation = arg_list_name_trainStation


class cGeneration_3_Valid:
    def __init__(self):
        self.path = r"res/generation_3_valide.txt"
        
        self.list_sentence = []
        self.list_csv_row = []

        self.list_name_city = []
        self.list_name_trainStation = []

        self.list_intention_depart = []
        self.list_mot_interrogatif = []
        self.list_intention_arriver = []        

        #
        self.propotion_city = 100

    def _add_csv_row(self, sentence):
        csv_row = []
        #ID
        csv_row.append("")
        #SENTENCE
        csv_row.append(sentence)
        #VALID
        csv_row.append(1)
        #ORIGIN
        csv_row.append("")
        #ARRIVAL
        csv_row.append("")
        #STEP_OVER
        csv_row.append("")
        #TYPE
        csv_row.append("")

        self.list_csv_row.append(csv_row)


    def read_File(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            rows = file.readlines()
            step = 0

            for i in range(len(rows)):
                row = rows[i]
                listText = row.split("\n")
                text = listText[0]
                if(text == "[Intention Depart]"):
                    step = 1
                    continue

                if(text == "[Mot interrogatif]"):
                    step = 2
                    continue

                if(text == "[Intention Arriver]"):
                    step = 3
                    continue

                if(text == "END"):
                    step = 0
                    continue

                if(text != ""):
                    match step:
                        case 1:
                            self.list_intention_depart.append(text)
                            continue
                        case 2:
                            self.list_mot_interrogatif.append(text)
                            continue
                        case 3:
                            self.list_intention_arriver.append(text)
                            continue
                        case _:
                            continue

    def generate_by_number(self, number):
        number_sentence_city = int((number*self.propotion_city)/100)
        for i in range(number):
            sentence = ""
            intention_depart = "En partant depuis"
            location_start = "TOULOUSE"
            mot_iterrogatif = "de quelle manière"
            intention_arriver = "se rendre à"
            location_end= "PARIS"
            

            if(len(self.list_intention_depart) > 0):
                index_intention_depart = random.randrange(len(self.list_intention_depart))
                intention_depart = self.list_intention_depart[index_intention_depart]

            if(len(self.list_mot_interrogatif) > 0):
                index_mot_interrogatif = random.randrange(len(self.list_mot_interrogatif))
                mot_iterrogatif = self.list_mot_interrogatif[index_mot_interrogatif]

            if(len(self.list_intention_arriver) > 0):
                index_intention_arriver = random.randrange(len(self.list_intention_arriver))
                intention_arriver = self.list_intention_arriver[index_intention_arriver]


            if(i <= number_sentence_city):
                if(len(self.list_name_city) > 0):
                    index_location_start = random.randrange(len(self.list_name_city))
                    location_start = self.list_name_city[index_location_start]

                    index_location_end = random.randrange(len(self.list_name_city))
                    location_end = self.list_name_city[index_location_end]
            else:
                if(len(self.list_name_trainStation) > 0):
                    index_location_start = random.randrange(len(self.list_name_trainStation))
                    location_start = self.list_name_city[index_location_start]

                    index_location_end = random.randrange(len(self.list_name_trainStation))
                    location_end = self.list_name_city[index_location_end]

            type_sentence = random.randint(1, 3)

            match type_sentence:
                case 1:
                    sentence = intention_depart + " " + location_start + " " + mot_iterrogatif + " " + intention_arriver + " " + location_end
                case 2:
                    sentence =  mot_iterrogatif + " " + intention_arriver + " " + location_end + " " + intention_depart + " " + location_start
                case 3:
                    sentence = mot_iterrogatif + " " + intention_depart + " " + location_start  + " " + intention_arriver + " " + location_end
            
            self.list_sentence.append(sentence)
            self._add_csv_row(sentence)

            
    def set_List_Name_City(self, arg_list_name_city):
        self.list_name_city = arg_list_name_city

    def set_List_Name_TrainStation(self, arg_list_name_trainStation):
        self.list_name_trainStation = arg_list_name_trainStation



class cGeneration_Invalide_Depuis:
    def __init__(self):
        self.path = r"res/generation_invalide_depuis.txt"
        
        self.list_sentence = []
        self.list_csv_row = []

        self.list_name_city = []
        self.list_name_trainStation = []

        self.list_temps_singulier = []
        self.list_temps_pluriel = []
        self.list_context = []

    
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


    def __get_temps(self):
        type_temps = random.randint(1, 2)

        match type_temps:
            case 1:
                return self.__get_temps_singulier()
            case 2 : 
                return self.__get_temps_pluriel()
            case _ :
                return ""

    def __get_temps_pluriel(self):
        if(len(self.list_temps_singulier) > 0):
                index_temps_singulier = random.randrange(len(self.list_temps_singulier))
                temps_singulier = self.list_temps_singulier[index_temps_singulier]

                return temps_singulier
        return ""

    def __get_temps_singulier(self):
        time = ""
        number_times = random.randint(1, 10)
        if(len(self.list_temps_pluriel) > 0):
                index_temps_pluriel = random.randrange(len(self.list_temps_pluriel))
                temps_pluriel = self.list_temps_pluriel[index_temps_pluriel]

                time = str(number_times) + " " +  temps_pluriel
                return time
        return ""

    def __get_context(self):
        if(len(self.list_context) > 0):
                index_context = random.randrange(len(self.list_context))
                context = self.list_context[index_context]
                return context
        return ""

    def __get_sentence(self, temps, context):
        sentence = ""
        type_sentence = random.randint(1, 2)
        if(type_sentence == 1):
            sentence = "Depuis" + " " + temps + " " + context
        elif(type_sentence == 2):
            sentence = context + " " + "depuis" + " " + temps
        return sentence 


    def read_File(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            rows = file.readlines()
            step = 0

            for i in range(len(rows)):
                row = rows[i]
                listText = row.split("\n")
                text = listText[0]
                if(text == "[Temps Singulier]"):
                    step = 1
                    continue

                if(text == "[Temps Pluriel]"):
                    step = 2
                    continue

                if(text == "[Context]"):
                    step = 3
                    continue

                if(text == "END"):
                    step = 0
                    continue

                if(text != ""):
                    match step:
                        case 1:
                            self.list_temps_singulier.append(text)
                            continue
                        case 2:
                            self.list_temps_pluriel.append(text)
                            continue
                        case 3:
                            self.list_context.append(text)
                            continue
                        case _:
                            continue

    def generate_by_number(self, number):
        for i in range(number):
            sentence = ""
            temps = ""
            context = ""

            temps = self.__get_temps()
            context = self.__get_context()
            sentence = self.__get_sentence(temps, context)

            if(not (sentence in self.list_sentence)):
                self.list_sentence.append(sentence)
                self.__add_csv_row(sentence)
            
    
    def set_List_Name_City(self, arg_list_name_city):
        self.list_name_city = arg_list_name_city

    def set_List_Name_TrainStation(self, arg_list_name_trainStation):
        self.list_name_trainStation = arg_list_name_trainStation



class cGenerateSentence:
    def __init__(self):
        self.c_list_des_gares = cListDesGares()


        self.c_generation_1_valid = cGeneration_1_Valid()
        self.c_generation_1_invalid = cGeneration_1_Invalid()

        self.c_generation_2_valid = cGeneration_2_Valid()
        self.c_generation_2_invalid = cGeneration_2_Invalid()

        self.c_generation_3_valid = cGeneration_3_Valid()

        self.c_generation_invalid_depuis = cGeneration_Invalide_Depuis()


        self.list_of_sentences = []
        self.list_csv_row = []

        self.path_csv = "generate_sentence.csv"


        self.__set_up()
        self.__set_list_name_city()
    

    def __generate_sentences(self, number):
        self.c_generation_1_valid.generate_by_number(number)
        self.c_generation_1_invalid.generate_by_number(number)

        self.c_generation_2_valid.generate_by_number(number)
        self.c_generation_2_invalid.generate_by_number(number)

        self.c_generation_3_valid.generate_by_number(number)

        number_sentence_depuis = int((20 *( number*5)) / 100) 
        self.c_generation_invalid_depuis.generate_by_number(number_sentence_depuis)


    def __get_list_of_sentences(self):
        self.list_of_sentences += self.c_generation_1_valid.list_sentence
        self.list_of_sentences += self.c_generation_1_invalid.list_sentence

        self.list_of_sentences += self.c_generation_2_valid.list_sentence
        self.list_of_sentences += self.c_generation_2_invalid.list_sentence

        self.list_of_sentences += self.c_generation_3_valid.list_sentence

        self.list_of_sentences += self.c_generation_invalid_depuis.list_sentence

    def __get_list_of_csv_row(self):
        self.list_csv_row += self.c_generation_1_valid.list_csv_row
        self.list_csv_row += self.c_generation_1_invalid.list_csv_row

        self.list_csv_row += self.c_generation_2_valid.list_csv_row
        self.list_csv_row += self.c_generation_2_invalid.list_csv_row

        self.list_csv_row += self.c_generation_3_valid.list_csv_row

        self.list_csv_row += self.c_generation_invalid_depuis.list_csv_row

    def __set_list_name_city(self):
        self.c_generation_1_valid.set_List_Name_City(self.c_list_des_gares.list_commune)
        self.c_generation_1_invalid.set_List_Name_City(self.c_list_des_gares.list_commune)

        self.c_generation_2_valid.set_List_Name_City(self.c_list_des_gares.list_commune)
        self.c_generation_2_invalid.set_List_Name_City(self.c_list_des_gares.list_commune)

        self.c_generation_3_valid.set_List_Name_City(self.c_list_des_gares.list_commune)

        self.c_generation_invalid_depuis.set_List_Name_City(self.c_list_des_gares.list_commune)


    def __set_up(self):
        self.c_list_des_gares.setUp()

        self.c_generation_1_valid.read_File()
        self.c_generation_1_invalid.read_File()

        self.c_generation_2_valid.read_File()
        self.c_generation_2_invalid.read_File()

        self.c_generation_3_valid.read_File()

        self.c_generation_invalid_depuis.read_File()


    def __write_csv(self):
        if not os.path.isfile(self.path_csv):
            with open(self.path_csv, 'w', newline='',encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile,delimiter=';')
                csv_writer.writerow(['ID','SENTENCE','VALID','ORIGIN','ARRIVAL','STEP_OVER','TYPE'])
            
        with open(self.path_csv, 'a', newline='',encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile,delimiter=';')
            
            for i in range(len(self.list_csv_row)):
                    row = self.list_csv_row[i]
                    row[0] = i
                    csv_writer.writerow(row)


    def generate_by_number(self, number):
        self.__generate_sentences(number)
        self.__get_list_of_sentences()
        self.__get_list_of_csv_row()
        self.__write_csv()
