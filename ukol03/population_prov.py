#!/usr/bin/env python3

from rdflib import Graph, BNode, Literal, Namespace, URIRef
from rdflib.namespace import RDF, PROV, FOAF

NSP = Namespace("https://github.com/DonRiccardo/UdDI/provenance#")
NSR = Namespace("https://github.com/DonRiccardo/UdDI/resources/")

def main():
    resultGraph = Graph(bind_namespaces="rdflib")

    createActivities(resultGraph)
    createAgents(resultGraph)
    createEntities(resultGraph)

    with open("population2021Prov.trig", "w", encoding="utf-8") as stream:
        stream.write(resultGraph.serialize(format="trig"))


def createAgents(collector: Graph):
    school = NSP.MFFUK
    collector.add((school, RDF.type, FOAF.Organization))
    collector.add((school, RDF.type, PROV.Agent))
    collector.add((school, FOAF.name, Literal("Matematicko-fyzikální fakulta, Univerzita Karlova", lang="cs")))
    collector.add((school, FOAF.homepage, URIRef("https://www.mff.cuni.cz/")))

    teacher = NSP.PetrSkoda
    collector.add((teacher, RDF.type, FOAF.Person))
    collector.add((teacher, RDF.type, PROV.Agent))
    collector.add((teacher, FOAF.givenName, Literal("Petr Škoda", lang="cs")))
    collector.add((teacher, FOAF.mbox, URIRef("mailto:petr.skoda@matfyz.cuni.cz")))
    collector.add((teacher, FOAF.homepage, URIRef("https://skodapetr.github.io/")))
    collector.add((teacher, PROV.actedOnBehalfOf, school))

    author = NSP.RichardHvizdos
    collector.add((author, RDF.type, FOAF.Person))
    collector.add((author, RDF.type, PROV.Agent))
    collector.add((author, FOAF.givenName, Literal("Richard Hvizdoš", lang="sk")))
    collector.add((author, FOAF.mbox, URIRef("mailto:hvizdosr@student.cuni.cz")))
    collector.add((author, FOAF.homepage, URIRef("https://github.com/DonRiccardo")))
    collector.add((author, PROV.actedOnBehalfOf, teacher))

    script = NSP.ScriptPopulation2021Cube
    collector.add((script, RDF.type, PROV.SoftwareAgent))
    collector.add((script, PROV.atLocation, Literal("file://homework01population.py")))
    collector.add((script, PROV.actedOnBehalfOf, author))

    scriptPrepareData = NSP.ScriptPrepareData
    collector.add((scriptPrepareData, RDF.type, PROV.SoftwareAgent))
    collector.add((scriptPrepareData, PROV.atLocation, Literal("file://prepareCSV_file.py")))
    collector.add((scriptPrepareData, PROV.actedOnBehalfOf, author))


def createEntities(collector: Graph):
    dataSet = NSR.Population2021Dataset
    collector.add((dataSet, RDF.type, PROV.entity))
    collector.add((dataSet, PROV.atLocation, URIRef("file://130141-22data2021.csv")))

    countyDataSet = NSR.CountryCodeListDataSet
    collector.add((countyDataSet, RDF.type, PROV.entity))
    collector.add((dataSet, PROV.atLocation, URIRef("file://číselník-okresů-vazba-101-nadřízený.csv")))    

    dataPrepared = NSR.PreparedDataSet
    collector.add((dataPrepared, RDF.type, PROV.entity))
    collector.add((dataPrepared, PROV.atLocation, Literal("file://preparedNRPZS.csv")))
    collector.add((dataPrepared, PROV.wasAttributedTo, NSP.ScriptPrepareData))
    collector.add((dataPrepared, PROV.wasDerivedFrom, dataSet))
    collector.add((dataPrepared, PROV.wasDerivedFrom, countyDataSet))
    collector.add((dataPrepared, PROV.wasGeneratedBy, NSP.PreparingData))


    dataCube = NSR.Population2021DataCube
    collector.add((dataCube, RDF.type, PROV.entity))
    collector.add((dataCube, PROV.atLocation, Literal("file://populationRDF.ttl")))
    collector.add((dataCube, PROV.wasAttributedTo, NSP.ScriptPopulation2021Cube))
    collector.add((dataCube, PROV.wasDerivedFrom, dataPrepared))
    collector.add((dataCube, PROV.wasGeneratedBy, NSP.Population2021CreateDataCube))

    

def createActivities(collector: Graph):
    usageDataCube = BNode()
    collector.add((usageDataCube, RDF.type, PROV.qualifiedUsage))
    collector.add((usageDataCube, PROV.hadRole, NSP.CSVdataset))
    collector.add((usageDataCube, PROV.entity, NSR.PreparedDataSet))

    createDataCube = NSP.Population2021CreateDataCube
    collector.add((createDataCube, RDF.type, PROV.activity))
    collector.add((createDataCube, PROV.wasAssociatedWith, NSP.RichardHvizdos))
    collector.add((createDataCube, PROV.used, NSR.PreparedDataSet))
    collector.add((createDataCube, PROV.generated, NSR.Population2021DataCube))
    collector.add((createDataCube, PROV.qualifiedUsage, usageDataCube))

    usagePreparingDataPopulation = BNode()
    collector.add((usagePreparingDataPopulation, RDF.type, PROV.qualifiedUsage))
    collector.add((usagePreparingDataPopulation, PROV.hadRole, NSP.CSVdataset))
    collector.add((usagePreparingDataPopulation, PROV.entity, NSR.Population2021Dataset))
    
    usagePreparingDataCountyCodeList= BNode()
    collector.add((usagePreparingDataCountyCodeList, RDF.type, PROV.qualifiedUsage))
    collector.add((usagePreparingDataCountyCodeList, PROV.hadRole, NSP.CSVdataset))
    collector.add((usagePreparingDataCountyCodeList, PROV.entity, NSR.CountryCodeListDataSet))

    preparingData = NSP.PreparingData
    collector.add((preparingData, RDF.type, PROV.activity))
    collector.add((preparingData, PROV.wasAssociatedWith, NSP.RichardHvizdos))
    collector.add((preparingData, PROV.used, NSR.CountryCodeListDataSet))
    collector.add((preparingData, PROV.used, NSR.Population2021Dataset))
    collector.add((preparingData, PROV.generated, NSR.PreparedDataSet))
    collector.add((preparingData, PROV.qualifiedUsage, usagePreparingDataPopulation))
    collector.add((preparingData, PROV.qualifiedUsage, usagePreparingDataCountyCodeList))

    collector.add((NSP.CSVdataset, RDF.type, PROV.Role))


if __name__ == "__main__":
    main()
