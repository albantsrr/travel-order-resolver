# generation.py
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
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Import
# -----------------------------------------------------------------------------
from src.classFile import *

import random
import time
import csv
import os
import argparse

class cGenerateSentence:
    def __init__(self):
        self.path_csv = r"sentence_generation.csv"
        self.list_Sentence = []
        self.list_csv_row = []
        self.id_row = 0

        self.csv = 0
        self.csv_writer = None

        # GENERATION 1
        self.pathGeneration_1 = r"res\generation_1.txt"
        self.listVerbe_gen1 = []

        # GENERATION 2
        self.pathGeneration_2 = r"res\generation_2.txt"
        self.listInterrogatif_gen2 = []
        self.listVerbe_gen2 = []
        self.listTrajet_gen2 = []

        # GENERATION 3
        self.pathGeneration_3 = r"res\generation_3.txt"
        self.listDepart_gen3 = []
        self.listInterrogatif_gen3 = []
        self.listArriver_gen3 = []

    def checkNameTrainStation(self,name):
        if("Gare" in name):
            return ("la " + name)
        else:
            return name

    def readGeneration(self,gen):
        match gen:
            case 0:
                self.readGeneration_1()
                self.readGeneration_2()
                self.readGeneration_3()
                return
            case 1:
                self.readGeneration_1()
                return
            case 2:
                self.readGeneration_2()
                return
            case 3:
                self.readGeneration_3()
                return

    def generate(self,number,gen):
        match gen:
            case 0:
                ratio = int(number/3)
                if(ratio < 1):
                    ratio = 0
                self.sentenceNum_1(ratio)
                self.sentenceNum_2(ratio)
                ratio = number - (ratio*2)
                if(ratio < 1):
                    ratio = 0
                self.sentenceNum_3(ratio)
                return
            case 1:
                self.sentenceNum_1(number)
                return
            case 2:
                self.sentenceNum_2(number)
                return
            case 3:
                self.sentenceNum_3(number)
                return

#   GENERATION 1
    def readGeneration_1(self):
        with open(self.pathGeneration_1, 'r', encoding='utf-8') as file:
            rows = file.readlines()
            step = 0

            for i in range(len(rows)):
                row = rows[i]
                listText = row.split("\n")
                text = listText[0]
                if(text == "[Verbe]"):
                    step = 1
                    continue

                if(text != ""):
                    match step:
                        case 1:
                            self.listVerbe_gen1.append(text)
                            continue
                        case _:
                            continue

    def sentenceNum_1(self,number):
        for i in range(number):
            sentence = ""
            verbeIdx = random.randrange(len(self.listVerbe_gen1))
            verbe  = self.listVerbe_gen1[verbeIdx] 
            
            nameOriginIdx = random.randrange(len(c_Stops.list_trainStationName))
            t_nameOrigin = c_Stops.list_trainStationName[nameOriginIdx]
            nameOrigin = self.checkNameTrainStation(t_nameOrigin)

            nameArrivalIdx = random.randrange(len(c_Stops.list_trainStationName))
            t_nameArrival = c_Stops.list_trainStationName[nameArrivalIdx]
            nameArrival = self.checkNameTrainStation(t_nameArrival)

            sentence = verbe + " de " +  nameOrigin + " à " +  nameArrival
            self.list_Sentence.append(sentence)

            if(self.csv):
                csv_row = []
                #ID
                csv_row.append(self.id_row)
                #SENTENCE
                csv_row.append(sentence)
                #VALID
                csv_row.append(1)
                #ORIGIN
                csv_row.append(t_nameOrigin)
                #ARRIVAL
                csv_row.append(t_nameArrival)
                #STEP_OVER
                csv_row.append("")

                self.list_csv_row.append(csv_row)
                self.id_row += 1

        # print(self.list_csv_row)      
        # print(self.list_Sentence)

    def sentence_1(self):
        print("GENERATION SENTENCE 1")
        count = 1
        total = len(c_Stops.list_trainStationName) * len(c_Stops.list_trainStationName) * len(self.listVerbe_gen1)
        step = int(total/100) 
        start_time = time.time()
        for i in range(len(c_Stops.list_trainStationName)):
            t_nameOrigin = c_Stops.list_trainStationName[i]
            nameOrigin = self.checkNameTrainStation(t_nameOrigin)
            for j in range(len(c_Stops.list_trainStationName)):
                if(j == i):
                    continue
                t_nameArrival = c_Stops.list_trainStationName[j]
                nameArrival = self.checkNameTrainStation(t_nameArrival)

                # verbeIdx = random.randrange(len(self.listVerbe_gen1))
                # verbe  = self.listVerbe_gen1[verbeIdx] 
                for k in range(len(self.listVerbe_gen1)):
                    verbe  = self.listVerbe_gen1[k] 

                    sentence = verbe + " de " +  nameOrigin + " à " +  nameArrival
                    self.list_Sentence.append(sentence)

                    if(self.csv):
                        csv_row = []
                        #ID
                        csv_row.append(self.id_row)
                        #SENTENCE
                        csv_row.append(sentence)
                        #VALID
                        csv_row.append(1)
                        #ORIGIN
                        csv_row.append(t_nameOrigin)
                        #ARRIVAL
                        csv_row.append(t_nameArrival)
                        #STEP_OVER
                        csv_row.append("")

                        self.list_csv_row.append(csv_row)
                        self.id_row += 1
                
                    count += 1
                    if((count % step) == 0):
                        end_time = time.time()
                        elapsed_time = end_time - start_time

                        remaining_time = ((elapsed_time*100)/int(count / step)) - elapsed_time 
                        print("{}%".format(int(count / step)))
                        print("  ==> {}/{}".format(count,total))
                        print("  Temps restant : {}s".format(int(remaining_time)))
                        print("\n")

        print("100%")
        print("  ==>{}".format(len(self.list_Sentence)))
   
#   GENERATION 2
    def readGeneration_2(self):
        with open(self.pathGeneration_2, 'r', encoding='utf-8') as file:
            rows = file.readlines()
            step = 0

            for i in range(len(rows)):
                row = rows[i]
                listText = row.split("\n")
                text = listText[0]
                if(text == "[Mot interrogatif]"):
                    step = 1
                    continue

                if(text == "[Verbe]"):
                    step = 2
                    continue

                if(text == "[Trajet]"):
                    step = 3
                    continue

                if(text != ""):
                    match step:
                        case 1:
                            self.listInterrogatif_gen2.append(text)
                            continue
                        case 2:
                            self.listVerbe_gen2.append(text)
                            continue
                        case 3:
                            self.listTrajet_gen2.append(text)
                            continue
                        case _:
                            continue

    def sentenceNum_2(self,number):
        for i in range(number):
            sentence = ""
            csv_row = []
            interrogatifIdx = random.randrange(len(self.listInterrogatif_gen2))
            interrogatif = self.listInterrogatif_gen2[interrogatifIdx]

            verbeIdx = random.randrange(len(self.listVerbe_gen2))
            verbe = self.listVerbe_gen2[verbeIdx]

            trajetIdx = random.randrange(len(self.listTrajet_gen2))
            trajet = self.listTrajet_gen2[trajetIdx]

            nameOriginIdx = random.randrange(len(c_Stops.list_trainStationName))
            t_nameOrigin = c_Stops.list_trainStationName[nameOriginIdx]
            nameOrigin = self.checkNameTrainStation(t_nameOrigin)

            nameArrivalIdx = random.randrange(len(c_Stops.list_trainStationName))
            t_nameArrival = c_Stops.list_trainStationName[nameArrivalIdx]
            nameArrival = self.checkNameTrainStation(t_nameArrival)

            sentence = interrogatif + " " + verbe + " " + trajet + " " + nameOrigin + " " + nameArrival

            if(self.csv):
                csv_row = []
                #ID
                csv_row.append(self.id_row)
                #SENTENCE
                csv_row.append(sentence)
                #VALID
                csv_row.append(1)
                #ORIGIN
                csv_row.append(t_nameOrigin)
                #ARRIVAL
                csv_row.append(t_nameArrival)
                #STEP_OVER
                csv_row.append("")

                self.list_csv_row.append(csv_row)
                self.id_row += 1
        
        # print(self.list_Sentence)

    def sentence_2(self):
        print("GENERATION SENTENCE 2")
        count = 1
        total = (len(c_Stops.list_trainStationName) * len(c_Stops.list_trainStationName) *len(self.listInterrogatif_gen2)
                  * len(self.listVerbe_gen2)* len(self.listTrajet_gen2))
        step = int(total/100) 
        start_time = time.time()
        for i in range(len(c_Stops.list_trainStationName)):
            t_nameOrigin = c_Stops.list_trainStationName[i]
            nameOrigin = self.checkNameTrainStation(t_nameOrigin)
            for j in range(len(c_Stops.list_trainStationName)):
                if(j == i):
                    continue
                t_nameArrival = c_Stops.list_trainStationName[j]
                nameArrival = self.checkNameTrainStation(t_nameArrival)
                for k in range(len(self.listInterrogatif_gen2)):
                    interrogatif = self.listInterrogatif_gen2[k]

                    for l in range(len(self.listVerbe_gen2)):
                        verbe  = self.listVerbe_gen2[l] 

                        for m in range(len(self.listTrajet_gen2)):
                            trajet = self.listTrajet_gen2[m]

                            sentence = interrogatif + " " + verbe + " " + trajet + " " + nameOrigin + " " + nameArrival
                            self.list_Sentence.append(sentence)

                            if(self.csv):
                                csv_row = []
                                #ID
                                csv_row.append(self.id_row)
                                #SENTENCE
                                csv_row.append(sentence)
                                #VALID
                                csv_row.append(1)
                                #ORIGIN
                                csv_row.append(t_nameOrigin)
                                #ARRIVAL
                                csv_row.append(t_nameArrival)
                                #STEP_OVER
                                csv_row.append("")

                                self.list_csv_row.append(csv_row)
                                self.id_row += 1
                        
                            count += 1
                            if((count % 10000) == 0):
                                print("coucou")
                            if((count % step) == 0):
                                end_time = time.time()
                                elapsed_time = end_time - start_time

                                remaining_time = ((elapsed_time*100)/int(count / step)) - elapsed_time 
                                print("{}%".format(int(count / step)))
                                print("  ==> {}/{}".format(count,total))
                                print("  Temps restant : {}s".format(int(remaining_time)))
                                print("\n")

        print("100%")
        print("  ==>{}".format(len(self.list_Sentence)))

#   GENERATION 3
    def readGeneration_3(self):
        with open(self.pathGeneration_3, 'r', encoding='utf-8') as file:
            rows = file.readlines()
            step = 0

            for i in range(len(rows)):
                row = rows[i]
                listText = row.split("\n")
                text = listText[0]
                if(text == "[Depart]"):
                    step = 1
                    continue

                if(text == "[Mot interrogatif]"):
                    step = 2
                    continue

                if(text == "[Arriver]"):
                    step = 3
                    continue

                if(text != ""):
                    match step:
                        case 1:
                            self.listDepart_gen3.append(text)
                            continue
                        case 2:
                            self.listInterrogatif_gen3.append(text)
                            continue
                        case 3:
                            self.listArriver_gen3.append(text)
                            continue
                        case _:
                            continue

    def sentenceNum_3(self,number):
        for i in range(number):
            sentence = ""
            departIdx = random.randrange(len(self.listDepart_gen3))
            depart = self.listDepart_gen3[departIdx]

            interrogatifIdx = random.randrange(len(self.listInterrogatif_gen3))
            interrogatif = self.listInterrogatif_gen3[interrogatifIdx]

            arriverIdx = random.randrange(len(self.listArriver_gen3))
            arriver = self.listArriver_gen3[arriverIdx]

            nameOriginIdx = random.randrange(len(c_Stops.list_trainStationName))
            t_nameOrigin = c_Stops.list_trainStationName[nameOriginIdx]
            nameOrigin = self.checkNameTrainStation(t_nameOrigin)

            nameArrivalIdx = random.randrange(len(c_Stops.list_trainStationName))
            t_nameArrival = c_Stops.list_trainStationName[nameArrivalIdx]
            nameArrival = self.checkNameTrainStation(t_nameArrival)

            sentence = depart + " " + nameOrigin + " " + interrogatif + " " + arriver + " " + nameArrival
            self.list_Sentence.append(sentence)

            if(self.csv):
                csv_row = []
                #ID
                csv_row.append(self.id_row)
                #SENTENCE
                csv_row.append(sentence)
                #VALID
                csv_row.append(1)
                #ORIGIN
                csv_row.append(t_nameOrigin)
                #ARRIVAL
                csv_row.append(t_nameArrival)
                #STEP_OVER
                csv_row.append("")

                self.list_csv_row.append(csv_row)
                self.id_row += 1
        
        # print(self.list_Sentence)

# CSV
    def setCSV(self,csv):
        self.csv = csv

    def setCSV_Name(self,name):
        self.path_csv = name + ".CSV"

    def writeCSV(self):
        if(self.csv!= 1):
            return
        
        if not os.path.isfile(self.path_csv):
            with open(self.path_csv, 'w', newline='',encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile,delimiter=';')
                csv_writer.writerow(['ID','SENTENCE','VALID','ORIGIN','ARRIVAL','STEP_OVER'])

        with open(self.path_csv, 'a', newline='',encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile,delimiter=';')
            for i in range(len(self.list_csv_row)):
                    row = self.list_csv_row[i]
                    csv_writer.writerow(row)

def MONITOR(arg_csv,arg_name,arg_gen,arg_nb):
    c_generateSentence = cGenerateSentence()
    c_generateSentence.setCSV(arg_csv)
    c_generateSentence.setCSV_Name(arg_name)
    c_generateSentence.readGeneration(arg_gen)
    c_generateSentence.generate(arg_nb,arg_gen)
    c_generateSentence.writeCSV()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', type=int, help='0 : disabled | 1 : enabled')
    parser.add_argument('--name', type=str,help='csv name')
    parser.add_argument('--gen', type=int, help='0 : all | 1 : sentence_1 | 2 : sentence_2 | 3 : sentence_3')
    parser.add_argument('--nb', type=int, help='setence number')

    args = parser.parse_args()
    
    arg_csv = 0
    arg_name = "sentence_generation"
    arg_gen = 0
    arg_nb = 100

    if args.csv:
        if(not(args.csv in [0,1])):
            print(f"<ERROR> --csv : {args.csv} isn't valid")
            return
        arg_csv = args.csv
    if args.name:
        arg_name = args.name 
    if args.gen:
        if(not(args.gen in [0,1,2,3])):
            print(f"<ERROR> --gen : {args.gen} isn't valid")
            return
        arg_gen = args.gen
    if args.nb:
        if(args.nb < 0):
            print(f"<ERROR> --nb : {args.gen} isn't valid")
            return
        arg_nb = args.nb

    MONITOR(arg_csv,arg_name,arg_gen,arg_nb)


if __name__ == "__main__":
    c_Stops = cStops()
    main()
