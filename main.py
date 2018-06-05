#!/usr/bin/python
# -*- coding: latin-1 -*-
from openpyxl import workbook, Workbook
import pandas as pd
import numpy as np
import io;
class main:

    path = ""  # path for data
    clusters = 0  # num of clusters
    runs = 0  # num of runs
    df = "";


    def setPath(self,path1):
        self.path = path1
    def setClusters(self,clusters1):
        self.clusters = clusters1
    def setRuns(self,run1):
        self.runs = run1
    def ReadCsv(self):
        self.df = pd.read_excel(open(self.path, 'rb'))
    def PrepareData(self):
        self.fill()
        self.Standart()
        self.grouping()
        #print dialog

    def fill(self):
        for col in list(self.df):
            if (col != 'country'):
                self.df[col].fillna(self.df[col].mean(), inplace=True)

    def Standart(self):
        for col in list(self.df):
            if col != 'country' and col != 'year':
                self.df[col] = self.df[col].apply(lambda x: ((x-self.df[col].mean())/self.df[col].std()))

    def grouping(self):
       self.df.drop(['year'],axis=1,inplace=True)
       self.df = self.df.pivot_table(self.df,index=['country'],aggfunc=np.mean)









if __name__ == "__main__":

    m = main()
    m.setPath('C:\\data.xlsx')
    m.ReadCsv()
    m.PrepareData()
    print (m.df)



