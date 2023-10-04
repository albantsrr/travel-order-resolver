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
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Import
# -----------------------------------------------------------------------------

class cStops:
    def __init__(self):
        self.path = r"./res/stops.txt"
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