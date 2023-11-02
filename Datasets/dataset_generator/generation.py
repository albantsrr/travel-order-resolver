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
# 16/10/2023 N. Laurens : add --p option (proportion of town names)
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

# old
if(0):
    class cGenerateSentence_old:
        def __init__(self):
            self.path_csv = r"sentence_generation.csv"
            self.list_Sentence = []
            self.list_csv_row = []
            self.id_row = 0

            self.list_station_name = [""]
            self.list_town_name = [""]

            self.csv = 0
            self.csv_writer = None

            self.verbose = 0

            self.proportion_town = 0.5 

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

        def setArg(self,verbose, proportion):
            self.verbose = verbose
            self.proportion_town = proportion

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
            if(self.verbose):
                print("GENERATION SENTENCE 1")
            count = 1
            total = number
            town_number_start = total - (total * self.proportion_town) 
            step = int(total/100) 
            if(step <= 0):
                step =1
            start_time = time.time()
            for i in range(number):
                sentence = ""
                verbeIdx = random.randrange(len(self.listVerbe_gen1))
                verbe  = self.listVerbe_gen1[verbeIdx] 
                
                if(i >= town_number_start):
                    nameOriginIdx = random.randrange(len(self.list_town_name))
                    nameArrivalIdx = random.randrange(len(self.list_town_name))

                    nameOrigin = self.list_town_name[nameOriginIdx]
                    nameArrival = self.list_town_name[nameArrivalIdx]

                    t_type = 2
                    
                else:
                    nameOriginIdx = random.randrange(len(self.list_station_name))
                    nameArrivalIdx = random.randrange(len(self.list_station_name))
                    t_nameOrigin = self.list_station_name[nameOriginIdx]
                    t_nameArrival = self.list_station_name[nameArrivalIdx]

                    nameOrigin = self.checkNameTrainStation(t_nameOrigin)
                    nameArrival = self.checkNameTrainStation(t_nameArrival)

                    t_type = 1
                    
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
                    csv_row.append(nameOrigin)
                    #ARRIVAL
                    csv_row.append(nameArrival)
                    #STEP_OVER
                    csv_row.append("")
                    #TYPE
                    csv_row.append(t_type)

                    self.list_csv_row.append(csv_row)
                    self.id_row += 1

                count += 1
                if(self.verbose != 1):
                    continue

                if((count % step) == 0):
                    end_time = time.time()
                    elapsed_time = end_time - start_time

                    remaining_time = ((elapsed_time*100)/int(count / step)) - elapsed_time 
                    print("Gen 1 -- {}%".format(int(count / step)))
                    print("  ==> {}/{}".format(count,total))
                    print("  Temps restant : {}s".format(int(remaining_time)))
                    print("\n")

            if(self.verbose):
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
            if(self.verbose ):
                print("GENERATION SENTENCE 2")
            count = 1
            total = number
            town_number_start = total - (total * self.proportion_town) 
            step = int(total/100) 
            if(step <= 0):
                step =1
            start_time = time.time()
            for i in range(number):
                sentence = ""
                csv_row = []
                interrogatifIdx = random.randrange(len(self.listInterrogatif_gen2))
                interrogatif = self.listInterrogatif_gen2[interrogatifIdx]

                verbeIdx = random.randrange(len(self.listVerbe_gen2))
                verbe = self.listVerbe_gen2[verbeIdx]

                trajetIdx = random.randrange(len(self.listTrajet_gen2))
                trajet = self.listTrajet_gen2[trajetIdx]
                if(i >= town_number_start):
                    nameOriginIdx = random.randrange(len(self.list_town_name))
                    nameArrivalIdx = random.randrange(len(self.list_town_name))

                    nameOrigin = self.list_town_name[nameOriginIdx]
                    nameArrival = self.list_town_name[nameArrivalIdx]

                    t_type = 2
                else:
                    nameOriginIdx = random.randrange(len(self.list_station_name))
                    nameArrivalIdx = random.randrange(len(self.list_station_name))
                    t_nameOrigin = self.list_station_name[nameOriginIdx]
                    t_nameArrival = self.list_station_name[nameArrivalIdx]

                    nameOrigin = self.checkNameTrainStation(t_nameOrigin)
                    nameArrival = self.checkNameTrainStation(t_nameArrival)

                    t_type = 1

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
                    csv_row.append(nameOrigin)
                    #ARRIVAL
                    csv_row.append(nameArrival)
                    #STEP_OVER
                    csv_row.append("")
                    #TYPE
                    csv_row.append(t_type)

                    self.list_csv_row.append(csv_row)
                    self.id_row += 1

                count += 1
                if(self.verbose != 1):
                    continue
                if((count % step) == 0):
                    end_time = time.time()
                    elapsed_time = end_time - start_time

                    remaining_time = ((elapsed_time*100)/int(count / step)) - elapsed_time 
                    print("Gen 2 -- {}%".format(int(count / step)))
                    print("  ==> {}/{}".format(count,total))
                    print("  Temps restant : {}s".format(int(remaining_time)))
                    print("\n")

            if(self.verbose):
                print("100%")
                print("  ==>{}".format(len(self.list_Sentence)))
            
            # print(self.list_Sentence)

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
            if(self.verbose):
                print("GENERATION SENTENCE 3")
            count = 1
            total = number
            town_number_start = total - (total * self.proportion_town) 
            step = int(total/100) 
            if(step <= 0):
                step =1
            start_time = time.time()
            for i in range(number):
                sentence = ""
                departIdx = random.randrange(len(self.listDepart_gen3))
                depart = self.listDepart_gen3[departIdx]

                interrogatifIdx = random.randrange(len(self.listInterrogatif_gen3))
                interrogatif = self.listInterrogatif_gen3[interrogatifIdx]

                arriverIdx = random.randrange(len(self.listArriver_gen3))
                arriver = self.listArriver_gen3[arriverIdx]
                if(i >= town_number_start):
                    nameOriginIdx = random.randrange(len(self.list_town_name))
                    nameArrivalIdx = random.randrange(len(self.list_town_name))

                    nameOrigin = self.list_town_name[nameOriginIdx]
                    nameArrival = self.list_town_name[nameArrivalIdx]

                    t_type = 2
                    
                else:
                    nameOriginIdx = random.randrange(len(self.list_station_name))
                    nameArrivalIdx = random.randrange(len(self.list_station_name))
                    t_nameOrigin = self.list_station_name[nameOriginIdx]
                    t_nameArrival = self.list_station_name[nameArrivalIdx]

                    nameOrigin = self.checkNameTrainStation(t_nameOrigin)
                    nameArrival = self.checkNameTrainStation(t_nameArrival)

                    t_type = 1

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
                    csv_row.append(nameOrigin)
                    #ARRIVAL
                    csv_row.append(nameArrival)
                    #STEP_OVER
                    csv_row.append("")
                    #TYPE
                    csv_row.append(t_type)

                    self.list_csv_row.append(csv_row)
                    self.id_row += 1

                count += 1
                if(self.verbose != 1):
                    continue
                if((count % step) == 0):
                    end_time = time.time()
                    elapsed_time = end_time - start_time

                    remaining_time = ((elapsed_time*100)/int(count / step)) - elapsed_time 
                    print("Gen 3 -- {}%".format(int(count / step)))
                    print("  ==> {}/{}".format(count,total))
                    print("  Temps restant : {}s".format(int(remaining_time)))
                    print("\n")

            if(self.verbose):
                print("100%")
                print("  ==>{}".format(len(self.list_Sentence)))
            
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
                    csv_writer.writerow(['ID','SENTENCE','VALID','ORIGIN','ARRIVAL','STEP_OVER','TYPE'])

            with open(self.path_csv, 'a', newline='',encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile,delimiter=';')
                if(self.verbose):
                    print("GENERATION CSV")
                count = 1
                total = len(self.list_csv_row)
                step = int(total/100) 
                start_time = time.time()
                for i in range(len(self.list_csv_row)):
                        row = self.list_csv_row[i]
                        csv_writer.writerow(row)

                        count += 1
                        if(self.verbose != 1):
                            continue
                        if((count % step) == 0):
                            end_time = time.time()
                            elapsed_time = end_time - start_time

                            remaining_time = ((elapsed_time*100)/int(count / step)) - elapsed_time 
                            print("CSV -- {}%".format(int(count / step)))
                            print("  ==> {}/{}".format(count,total))
                            print("  Temps restant : {}s".format(int(remaining_time)))
                            print("\n")
                if(self.verbose):
                    print("100%")
                    print("  ==>{}".format(total))

    # SET
        def set_List_Station_Name(self,new_list_station_name):
            self.list_station_name = new_list_station_name

        def set_List_Town_Name(self,new_list_town_name):
            self.list_town_name = new_list_town_name

    def MONITOR(arg_csv, arg_name, arg_gen, arg_nb, arg_p, arg_v):
        c_timeTables = cTimeTables()
        c_timeTables.setUp()

        c_listDesGares = cListDesGares()
        c_listDesGares.setUp()

        c_generateSentence = cGenerateSentence()

        c_generateSentence.set_List_Station_Name(c_timeTables.list_trainStationName)
        c_generateSentence.set_List_Town_Name(c_listDesGares.list_commune)

        c_generateSentence.setCSV(arg_csv)
        c_generateSentence.setCSV_Name(arg_name)
        c_generateSentence.setArg(arg_v, arg_p)
        c_generateSentence.readGeneration(arg_gen)
        c_generateSentence.generate(arg_nb,arg_gen)
        c_generateSentence.writeCSV()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', type=int, help='0 : disabled | 1 : enabled')
    parser.add_argument('--name', type=str,help='csv name')
    parser.add_argument('--gen', type=int, help='0 : all | 1 : sentence_1 | 2 : sentence_2 | 3 : sentence_3')
    parser.add_argument('--nb', type=int, help='setence number')
    parser.add_argument('--p', type=int, help='town proportion : [0-100]')
    parser.add_argument('--v', type=int, help='verbose : 0 | 1')

    args = parser.parse_args()
    
    arg_csv = 0
    arg_name = "sentence_generation"
    arg_gen = 0
    arg_nb = 100
    arg_p = 50
    arg_v = 0

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

    if args.p:
        if(args.p < 0 or args.p > 100):
            print(f"<ERROR> --p : {args.p} isn't valid")
            return
        arg_p = (args.p / 100)

    if args.v:
        if(not(args.v in [0,1])):
            print(f"<ERROR> --v : {args.v} isn't valid")
            return
        arg_v = args.v

    # MONITOR(arg_csv, arg_name, arg_gen, arg_nb, arg_p, arg_v)

if __name__ == "__main__":
    generation = cGenerateSentence()
    generation.generate_by_number(10000)
    # main()