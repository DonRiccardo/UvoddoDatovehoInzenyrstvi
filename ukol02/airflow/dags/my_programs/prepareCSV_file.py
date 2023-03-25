#!/usr/bin/env python
# coding: utf-8

# # Príprava dát pre domácu úlohu
def prepareDataForProcessing():
    # In[1]:


    import pandas as pd


    # ## Poskytovatelé zdravotních služeb

    # In[2]:


    nrpzs = pd.read_csv("./narodni-registr-poskytovatelu-zdravotnich-sluzeb.csv", low_memory=False)
    nrpzs.head(10)


    # In[6]:


    n = nrpzs.groupby(['OkresCode', 'KrajCode', 'OborPece']).size().reset_index(name='POCET')
    n


    # In[7]:


    n.to_csv("./preparedNRPZS.csv")


    # ## Obyvatelé okresy 2021

    # In[11]:


    dataObyv = pd.read_csv("./130141-22data2021.csv")
    stred = dataObyv[dataObyv["vuk"]=="DEM0004"]

    okresKraj = [101]

    stredOkresKraj = stred[stred.vuzemi_cis.isin(okresKraj)]
    stredOkresKraj


    # In[12]:


    ciselnik = pd.read_csv("./číselník-okresů-vazba-101-nadřízený.csv")
    ciselnik


    # In[13]:


    stredOkresKod = stredOkresKraj.merge(ciselnik, left_on="vuzemi_kod", right_on="CHODNOTA2")
    stredOkresKod


    # In[38]:


    stredOkresKod.to_csv("./preparedMeanPocet.csv")

if __name__ == "__main__":
    prepareDataForProcessing()