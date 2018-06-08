#!/usr/bin/python
# -*- coding: latin-1 -*-
from openpyxl import workbook, Workbook
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from itertools import cycle
from matplotlib import colors
import plotly.plotly as py




class model:

    path = ""  # path for data
    clusters = 0  # num of clusters
    runs = 0  # num of runs
    df = "" # the dataframe that contains the data

    #######--------Initialise---------###
    def initBeforePrepare(self,path1,clusters1,run1):
        self.setPath(path1)
        self.setClusters(clusters1)
        self.setRuns(run1)
        self.ReadCsv(self.path)

    def setPath(self,path1):
        self.path = path1

    def setClusters(self,clusters1):
        self.clusters = clusters1

    def setRuns(self,run1):
        self.runs = run1

    def ReadCsv(self,path):
        self.df = pd.read_excel(open(path, 'rb'))

    #######--------Data prep---------###
    ###Prepering the data###
    def PrepareData(self):
        self.ReadCsv(self.path)
        self.fill()
        self.Standart()
        self.grouping()

    ###fill the empty cells with avg###
    def fill(self):
        for col in list(self.df):
            if col != 'country' and col != 'year':
                self.df[col].fillna(self.df[col].mean(), inplace=True)

    ###Perfom Standardization on the data###
    def Standart(self):
        for col in list(self.df):
            if col != 'country' and col != 'year':
                self.df[col] = self.df[col].apply(lambda x: ((x-self.df[col].mean())/self.df[col].std()))

    ###Group by the data by countires###
    def grouping(self):
       self.df.drop(['year'],axis=1,inplace=True)
       self.df = self.df.pivot_table(self.df,index=['country'],aggfunc=np.mean)

    #######--------K-means Model---------###
    ###The K-means model and after prints###
    def KmeansModel(self):
       kmeans = KMeans(n_clusters=self.clusters, n_init=self.runs).fit_predict(self.df)
       self.df.reset_index(inplace=True)
       self.df['cluster'] = pd.Series(kmeans)
       self.PrintByScatter()
       self.PrintMap()

    ###Printing result of the kmeans by scatter###
    def PrintByScatter(self):
        N = self.clusters
        colorlist = list(colors.ColorConverter.colors.keys())
        cycol = cycle('bgrcmk')
        for i in range(len(self.df)):
            plt.scatter(self.df['Social support'][i], self.df['Generosity'][i],color=colorlist[self.df['cluster'][i]])
        plt.xlabel("Social support")
        plt.ylabel("Generosity")
        plt.title("Generosity by Social support Graph ")
        plt.savefig("scatter.png")

    #print the result using choropleth
    def PrintMap(self):
        py.sign_in('YR23','MIMIz9so6Ac3yMcxp8HL')
        scl = [[0.0, 'rgb(242,240,247)'], [0.2, 'rgb(218,218,235)'], [0.4, 'rgb(188,189,220)'], \
               [0.6, 'rgb(158,154,200)'], [0.8, 'rgb(117,107,177)'], [1.0, 'rgb(84,39,143)']]

        data = [dict(
            type='choropleth',
            colorscale=scl,
            autocolorscale=False,
            locations=self.df['country'],
            z=self.df['cluster'],
            locationmode='country names',
            marker=dict(
                line=dict(
                    color='rgb(255,255,255)',
                    width=2
                )),
            colorbar=dict(
                title="Clusters")
        )]

        layout = dict(
            title='Clusters by the K-means model ',
            geo=dict(
                scope='world',
                projection=dict(type='natural earth'),
                showlakes=True,
                lakecolor='rgb(255, 255, 255)'),
        )

        fig = dict(data=data, layout=layout)
        py.plot(fig, filename='d3-cloropleth-map')
        py.image.save_as(fig, filename='name.png')








