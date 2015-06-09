from logicOR import LogicOR
from logicAND import LogicAND
from logicNO import LogicNO
from time import sleep
import re

class MainLogic():

    def __init__(self, parent):
        self.allElements = list()
        self.beginPosition = list()
        self.endPosition = set()
        self.allConditions = dict()

    def calcScheme(self):
        thisIsTheEnd = False
        while (not thisIsTheEnd):
            for e in self.allElements:
                pinState = list(e.input)
                allReady = True
                values = list()
                for p in pinState:
                    #print(e.input)
                    q = self.allConditions[p]
                    if q["wrkd"] == 0:
                        allReady = False
                        break
                    else:
                        values.append(q["value"])

                if allReady:
                    c = e.calc(values)
                    #print("element ready ", c, " ", values)
                    pinState = e.output
                    for p in pinState:
                        self.allConditions[p] = {"wrkd": 1, "value": c}

            thisIsTheEnd = True
            for t in self.allConditions.keys():
                t = self.allConditions[t]
                if t["wrkd"] == 0:
                    thisIsTheEnd = False
                    break
            #sleep(0.4)

    def fileParser(self):
        f = open('in.txt', 'r')
        for line in f:
            line = re.split("\s+", line.strip())
            line[0] = line[0].lower()
            if len(line) < 2: #Элемент без соединений, пропускаем
                continue

            line[1] = re.split("[,|\s]*", line[1])

            if len(line) < 3:
                if line[0].find("out") > -1:
                    self.endPosition |= set(line[1])
                    for q in line[1]:
                        self.allConditions[q] = {"wrkd": 0, "value": 0}

                if line[0].find("in") > -1:
                    self.beginPosition.append(line[1])
                    #print(beginPosition, line[1])
                    for q in line[1]:
                        self.allConditions[q] = {"wrkd": 1, "value": 0}
            else:
                outlist = re.split("[,|\s]*", line[2])
                inlist = line[1]
                t = None
                if line[0].find("or") > -1:
                    t = LogicOR(inlist, outlist)
                elif line[0].find("and") > -1:
                    t = LogicAND(inlist, outlist)
                elif line[0].find("no") > -1:
                    t = LogicNO(inlist, outlist)
                self.allElements.append(t)
                for q in outlist:
                    self.allConditions[q] = {"wrkd": 0, "value": 0}
        print(self.allConditions)
        print(self.allElements)
        f.close()

    def genInputValues(self):
        print("Processing...")
        result = list()
        countVar = 2**len(self.beginPosition)
        print("Всего вариантов,", countVar)
        for i in range(0, countVar):
            beginValue = list(bin(i)[2:].zfill(len(self.beginPosition)))

            for i, p in enumerate(self.beginPosition):
                for p1 in p:
                    self.allConditions[p1] = {"wrkd": 1, "value": beginValue[i]}

            self.calcScheme()
            endvalue = list()
            for p in self.endPosition:
                q = self.allConditions[p]
                endvalue.append(q["value"])
            print("value", beginValue, " ", endvalue)
            t = list(beginValue)
            t.append(endvalue)
            result.append(t)

        return len(self.beginPosition), result

m = MainLogic(None)
m.fileParser()
m.genInputValues()
