# coding: utf-8
"""
Segmentation Script for Myanmar Characters

Originally written by Ye Kyaw Thu (https://github.com/ye-kyaw-thu)
Revised by Phone Thant Ko (https://github.com/phonethantko)
"""
import re
from nltk import ngrams
import itertools
import sys

class Segmentation:
    texts = None
    matchlist, result, stopwordslist = [], [], []
    def __init__(self, textArray):
        self.texts = textArray
        matchlist = []
        wlist = []
        with open("wordlist.txt", encoding = 'utf8') as filehandle:
            wlist = filehandle.readlines()
        self.result = []

    def trigram(self, inputstring):
        data = self.segment(inputstring)
        text = inputstring
        temp = []

        val = self.tokenize(data,4)

        if len(val['dd']) != 0:
            temp.extend(val['mm'])
            val1 = self.tokenize(val['dd'],3)

            if len(val1['dd']) != 0:

                temp.extend(val1['mm'])
                val2 = self.tokenize(val1['dd'],2)

                if len(val2['dd']) != 0:

                    temp.extend(val2['mm'])
                    #temp.extend(val2['dd'])
                else:
                    var = ""

            else:
                temp.extend(val1['mm'])
        else:
            temp.extend(val['mm'])


        for t in temp:
            if t in text:
                text = text.replace(t," "+t+" ")

        finallist = []
        tmpdict = {}
        for i,val in enumerate(text.split()):
            tmpdict[i] = val
        for i in tmpdict:

            if tmpdict[i] in temp:
                finallist.append(tmpdict[i])
            else:
                s = self.segment(tmpdict[i])
                finallist.extend(s)
        self.result.append(finallist)

        fffopen = open("segmentedfile.txt","a+",encoding = "utf-8-sig")
        for rr in finallist:
            fffopen.write(rr+"\n")

    def tokenize(self,data,n):
        FGMatch = []
        text = "".join(data)

        templist = []
        tt = ngrams(data,n)
        for aa in tt:
            i = "".join(aa)
            temp = ""

            ss = self.matchText(i)
            if ss['flag'] == True:
                FGMatch.append(ss['val'])
                temp = text.replace(ss['val'],'')
                text = temp
                templist.append(text)

            else:
                templist.append(text)
                continue

        try:
            result = {'dd':self.segment(templist[-1]),'mm':FGMatch}
        except:
            result = {'dd':data,'mm':FGMatch}
        return result

    def segment(self, text):
        text = re.sub(r'(?:(?<!္)([က-ဪဿ၊-၏]|[၀-၉]+|[^က-၏]+)(?![ှျ]?[့္်]))',r's\1',text).strip('s').split('s')
        return text

    def matchText(self,text):

        wordVal = {'flag':False, 'val':''}
        for w in self.matchlist:
            if text == w:
                wordVal['flag'] = True
                wordVal['val'] = text

        return wordVal

    def runSegmentation(self):
        for t in self.texts:
            t = t.rstrip()
            self.trigram(t)

        preresult = []
        for i in self.result:
            tempp = ""
            for ff in i:
                if (len(i)>0):
                    if ff == i[-1]:
                        tempp += ff
                    else:
                        tempp += ff+" "

            preresult.append(tempp)

        for i, t in enumerate(preresult):
            self.texts[i] = t
        return self.texts