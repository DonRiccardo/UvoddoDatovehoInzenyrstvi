#!/usr/bin/env python
# coding: utf-8

def prepareDataForProcessing():
    # # Príprava dát pre domácu úlohu

    # In[2]:


    import pandas as pd


    # ## Poskytovatelé zdravotních služeb

    # In[3]:


    nrpzs = pd.read_csv("./narodni-registr-poskytovatelu-zdravotnich-sluzeb.csv", low_memory=False)
    nrpzs.head(10)


    # In[25]:


    n = nrpzs.groupby(['OkresCode','Okres', 'KrajCode', 'Kraj', 'OborPece']).size().reset_index(name='POCET')
    n


    # In[27]:


    n = n.assign(ID_obor_pece=(n["OborPece"]).astype("category").cat.codes)


    # In[29]:


    n["OborPece"].unique().__len__()


    # In[30]:


    n["ID_obor_pece"].unique().__len__()


    # In[37]:


    n.to_csv("preparedNRPZS.csv")


    # ## Obyvatelé okresy 2021

    # In[4]:


    dataObyv = pd.read_csv("./130141-22data2021.csv")
    stred = dataObyv[dataObyv["vuk"]=="DEM0004"]

    okresKraj = [101]

    stredOkresKraj = stred[stred.vuzemi_cis.isin(okresKraj)]
    stredOkresKraj


    # In[5]:


    ciselnik = pd.read_csv("./číselník-okresů-vazba-101-nadřízený.csv")
    ciselnik


    # In[6]:


    stredOkresKod = stredOkresKraj.merge(ciselnik, left_on="vuzemi_kod", right_on="CHODNOTA2")
    stredOkresKod


    # In[16]:


    stredOkresKod["Kód NUTS3 kraje"] = stredOkresKod["CHODNOTA1"].apply(lambda x : x[:-1])


    # In[17]:


    stredOkresKod


    # In[9]:


    stredOkresKod.to_csv("preparedMeanPocet.csv")

if __name__ == "__main__":
    prepareDataForProcessing()