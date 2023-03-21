#!/usr/bin/env python3
import csv

from rdflib import Graph, BNode, Literal, Namespace, URIRef
from rdflib.namespace import QB, RDF, XSD, SKOS, DCTERMS


NS = Namespace("https://github.com/DonRiccardo/UdDI/ontology#")
NSR = Namespace("https://github.com/DonRiccardo/UdDI/resources/")
DBO = Namespace("https://dbpedia.org/ontology/")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
SDMXDIMENSION = Namespace("http://purl.org/linked-data/sdmx/2009/dimension#")
SDMXMEASURE = Namespace("http://purl.org/linked-data/sdmx/2009/measure#")




def main():
    dataCSV = load_csv_file_as_object("prepare_data/preparedNRPZS.csv")
    dataCube = creatingGraph(dataCSV)
    with open("careRDF.ttl", "w", encoding="utf-8") as stream:
        stream.write(dataCube.serialize(format="ttl"))
    #print(dataCube.serialize(format="ttl"))
    print("-" * 80)


def creatingGraph(data):
    result = Graph()
    dimensions = createDimensions(result)
    measure = createMeasure(result)
    structure = createStructure(result, dimensions, measure)
    dataset = createDataset(result, structure)
    createObservations(result, dataset, data)
    return result



def createDimensions(collector: Graph):
    okres = DBO.county
    collector.add((okres, RDF.type, RDFS.Property))
    collector.add((okres, RDF.type, QB.DimensionProperty))
    collector.add((okres, SKOS.prefLabel, Literal("okres", lang="cs")))
    collector.add((okres, SKOS.prefLabel, Literal("county", lang="en")))
    collector.add((okres, RDFS.subPropertyOf, SDMXDIMENSION.refArea))

    kraj = DBO.region
    collector.add((kraj, RDF.type, RDFS.Property))
    collector.add((kraj, RDF.type, QB.DimensionProperty))
    collector.add((kraj, SKOS.prefLabel, Literal("kraj", lang="cs")))
    collector.add((kraj, SKOS.prefLabel, Literal("region", lang="en")))
    collector.add((kraj, RDFS.subPropertyOf, SDMXDIMENSION.refArea))

    oborPece = DBO.specialist
    collector.add((oborPece, RDF.type, RDFS.Property))
    collector.add((oborPece, RDF.type, QB.DimensionProperty))
    collector.add((oborPece, SKOS.prefLabel, Literal("obor péče", lang="cs")))
    collector.add((oborPece, SKOS.prefLabel, Literal("field of care", lang="en")))
    collector.add((oborPece, RDFS.subPropertyOf, SDMXDIMENSION.occupation))

    return [okres, kraj, oborPece]

def createMeasure(collector: Graph):
    pocet = NS.pocetPoskytovateluPece
    collector.add((pocet, RDF.type, RDFS.Property))
    collector.add((pocet, RDF.type, QB.MeasureProperty))
    collector.add((pocet, SKOS.prefLabel, Literal("počet poskytovatelů péče", lang="cs")))
    collector.add((pocet, SKOS.prefLabel, Literal("number of care providers", lang="en")))
    collector.add((pocet, RDFS.subPropertyOf, SDMXMEASURE.obsValue))
    collector.add((pocet, RDFS.range, XSD.integer))

    return [pocet]


def createStructure(collector: Graph, dimensions, measures):
    structure = NS.structure
    collector.add((structure, RDF.type, QB.MeasureProperty ))

    for dimension in dimensions:
        component = BNode()
        collector.add((structure, QB.component, component))
        collector.add((component, QB.dimension, dimension))

    for measure in measures:
        component = BNode()
        collector.add((structure, QB.component, component))
        collector.add((component, QB.measure, measure))

    return structure


def createObservations(collector: Graph, dataset, data):
    for index, row in enumerate(data):
        resource = NSR["observation-" + str(index).zfill(3)]
        createObservation(collector, dataset, resource, row)


def createObservation(collector: Graph, dataset, resource, data):
    collector.add((resource, RDF.type, QB.Observation))
    collector.add((resource, QB.dataSet, dataset))
    collector.add((resource, DBO.county, URIRef("https://github.com/DonRiccardo/"+data["OkresCode"])))
    collector.add((resource, DBO.region, URIRef("https://github.com/DonRiccardo/"+data["KrajCode"])))
    collector.add((resource, DBO.specialist, Literal(data["OborPece"], datatype=XSD.string)))
    collector.add((resource, NS.pocetPoskytovateluPece, Literal(data["POCET"], datatype=XSD.integer)))
    




def createDataset(collector: Graph, structure):

    dataset = NSR.dataCubeInstance
    collector.add((dataset, RDF.type, QB.DataSet))
    collector.add((dataset, DCTERMS.publisher, URIRef("https://github.com/DonRiccardo/")))
    collector.add((dataset, DCTERMS.available, Literal("2023-03-10", datatype=XSD.date)))
    collector.add((dataset, DCTERMS.language, Literal("cs", datatype=XSD.language)))
    collector.add((dataset, DCTERMS.language, Literal("en", datatype=XSD.language)))
    collector.add((dataset, DCTERMS.license, URIRef("https://github.com/DonRiccardo/UdDI/blob/d0291e5a83fc1bfcafb95b48fe7b241e13cc254d/ukol01/license.txt")))
    collector.add((dataset, SKOS.prefLabel, Literal("number of care providers", lang="en")))
    collector.add((dataset, SKOS.prefLabel, Literal("počet poskytovatelů péče", lang="cs")))
    collector.add((dataset, QB.structure, structure))

    return dataset




def load_csv_file_as_object(file_path: str):
    result = []
    with open(file_path, "r", encoding="utf-8") as stream:
        reader = csv.reader(stream)
        header = next(reader)  # Skip header
        for line in reader:
            result.append({key: value for key, value in zip(header, line)})
    return result


if __name__ == "__main__":
    main();