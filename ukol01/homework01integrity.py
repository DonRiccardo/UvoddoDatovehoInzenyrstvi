#!/usr/bin/env python3

import rdflib

filenameCare = "./careRDF.ttl"
filenamePopulation = "./populationRDF.ttl"



ICqueries =[
"""
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
PREFIX qb:      <http://purl.org/linked-data/cube#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
ASK {
  {
    # Check observation has a data set
    ?obs a qb:Observation .
    FILTER NOT EXISTS { ?obs qb:dataSet ?dataset1 . }
  } UNION {
    # Check has just one data set
    ?obs a qb:Observation ;
       qb:dataSet ?dataset1, ?dataset2 .
    FILTER (?dataset1 != ?dataset2)
  }
}
 
""",
"""
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
PREFIX qb:      <http://purl.org/linked-data/cube#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>

ASK {
  {
    # Check dataset has a dsd
    ?dataset a qb:DataSet .
    FILTER NOT EXISTS { ?dataset qb:structure ?dsd . }
  } UNION { 
    # Check has just one dsd
    ?dataset a qb:DataSet ;
       qb:structure ?dsd1, ?dsd2 .
    FILTER (?dsd1 != ?dsd2)
  }
}
""",
"""
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
PREFIX qb:      <http://purl.org/linked-data/cube#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>

ASK {
  ?dsd a qb:DataStructureDefinition .
  FILTER NOT EXISTS { ?dsd qb:component [qb:componentProperty [a qb:MeasureProperty]] }
}
""",
"""
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
PREFIX qb:      <http://purl.org/linked-data/cube#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>

ASK {
  ?dim a qb:DimensionProperty .
  FILTER NOT EXISTS { ?dim rdfs:range [] }
}
""",
"""
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
PREFIX qb:      <http://purl.org/linked-data/cube#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
ASK {
  ?dim a qb:DimensionProperty ;
       rdfs:range skos:Concept .
  FILTER NOT EXISTS { ?dim qb:codeList [] }
}
""",
"""
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
PREFIX qb:      <http://purl.org/linked-data/cube#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
ASK {
  ?dsd qb:component ?componentSpec .
  ?componentSpec qb:componentRequired "false"^^xsd:boolean ;
                 qb:componentProperty ?component .
  FILTER NOT EXISTS { ?component a qb:AttributeProperty }
}
""",
"""
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
PREFIX qb:      <http://purl.org/linked-data/cube#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
ASK {
    ?sliceKey a qb:SliceKey .
    FILTER NOT EXISTS { [a qb:DataStructureDefinition] qb:sliceKey ?sliceKey }
}
""",
"""
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
PREFIX qb:      <http://purl.org/linked-data/cube#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
ASK {
  ?slicekey a qb:SliceKey;
      qb:componentProperty ?prop .
  ?dsd qb:sliceKey ?slicekey .
  FILTER NOT EXISTS { ?dsd qb:component [qb:componentProperty ?prop] }
}
""",
"""
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
PREFIX qb:      <http://purl.org/linked-data/cube#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
ASK {
  {
    # Slice has a key
    ?slice a qb:Slice .
    FILTER NOT EXISTS { ?slice qb:sliceStructure ?key }
  } UNION {
    # Slice has just one key
    ?slice a qb:Slice ;
           qb:sliceStructure ?key1, ?key2;
    FILTER (?key1 != ?key2)
  }
}
""",
"""
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
PREFIX qb:      <http://purl.org/linked-data/cube#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
ASK {
  ?slice qb:sliceStructure [qb:componentProperty ?dim] .
  FILTER NOT EXISTS { ?slice ?dim [] }
}
  
""",
"""
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
PREFIX qb:      <http://purl.org/linked-data/cube#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
ASK {
    ?obs qb:dataSet/qb:structure/qb:component/qb:componentProperty ?dim .
    ?dim a qb:DimensionProperty;
    FILTER NOT EXISTS { ?obs ?dim [] }
}
    
""",
"""
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
PREFIX qb:      <http://purl.org/linked-data/cube#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
ASK {
  FILTER( ?allEqual )
  {
    # For each pair of observations test if all the dimension values are the same
    SELECT (MIN(?equal) AS ?allEqual) WHERE {
        ?obs1 qb:dataSet ?dataset .
        ?obs2 qb:dataSet ?dataset .
        FILTER (?obs1 != ?obs2)
        ?dataset qb:structure/qb:component/qb:componentProperty ?dim .
        ?dim a qb:DimensionProperty .
        ?obs1 ?dim ?value1 .
        ?obs2 ?dim ?value2 .
        BIND( ?value1 = ?value2 AS ?equal)
    } GROUP BY ?obs1 ?obs2
  }
}
""",
"""
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
PREFIX qb:      <http://purl.org/linked-data/cube#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
ASK {
    ?obs qb:dataSet/qb:structure/qb:component ?component .
    ?component qb:componentRequired "true"^^xsd:boolean ;
               qb:componentProperty ?attr .
    FILTER NOT EXISTS { ?obs ?attr [] }
}
""",
"""
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
PREFIX qb:      <http://purl.org/linked-data/cube#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
ASK {
    # Observation in a non-measureType cube
    ?obs qb:dataSet/qb:structure ?dsd .
    FILTER NOT EXISTS { ?dsd qb:component/qb:componentProperty qb:measureType }

    # verify every measure is present
    ?dsd qb:component/qb:componentProperty ?measure .
    ?measure a qb:MeasureProperty;
    FILTER NOT EXISTS { ?obs ?measure [] }
}
""",
"""
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
PREFIX qb:      <http://purl.org/linked-data/cube#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
ASK {
    # Observation in a measureType-cube
    ?obs qb:dataSet/qb:structure ?dsd ;
         qb:measureType ?measure .
    ?dsd qb:component/qb:componentProperty qb:measureType .
    # Must have value for its measureType
    FILTER NOT EXISTS { ?obs ?measure [] }
}
""",
"""
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
PREFIX qb:      <http://purl.org/linked-data/cube#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
ASK {
    # Observation with measureType
    ?obs qb:dataSet/qb:structure ?dsd ;
         qb:measureType ?measure ;
         ?omeasure [] .
    # Any measure on the observation
    ?dsd qb:component/qb:componentProperty qb:measureType ;
         qb:component/qb:componentProperty ?omeasure .
    ?omeasure a qb:MeasureProperty .
    # Must be the same as the measureType
    FILTER (?omeasure != ?measure)
}
""",
"""
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
PREFIX qb:      <http://purl.org/linked-data/cube#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
ASK {
  {
      # Count number of other measures found at each point 
      SELECT ?numMeasures (COUNT(?obs2) AS ?count) WHERE {
          {
              # Find the DSDs and check how many measures they have
              SELECT ?dsd (COUNT(?m) AS ?numMeasures) WHERE {
                  ?dsd qb:component/qb:componentProperty ?m.
                  ?m a qb:MeasureProperty .
              } GROUP BY ?dsd
          }
        
          # Observation in measureType cube
          ?obs1 qb:dataSet/qb:structure ?dsd;
                qb:dataSet ?dataset ;
                qb:measureType ?m1 .
    
          # Other observation at same dimension value
          ?obs2 qb:dataSet ?dataset ;
                qb:measureType ?m2 .
          FILTER NOT EXISTS { 
              ?dsd qb:component/qb:componentProperty ?dim .
              FILTER (?dim != qb:measureType)
              ?dim a qb:DimensionProperty .
              ?obs1 ?dim ?v1 . 
              ?obs2 ?dim ?v2. 
              FILTER (?v1 != ?v2)
          }
          
      } GROUP BY ?obs1 ?numMeasures
        HAVING (?count != ?numMeasures)
  }
}
""",
"""
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
PREFIX qb:      <http://purl.org/linked-data/cube#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
ASK {
    ?dataset qb:slice       ?slice .
    ?slice   qb:observation ?obs .
    FILTER NOT EXISTS { ?obs qb:dataSet ?dataset . }
}
""",
"""
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
PREFIX qb:      <http://purl.org/linked-data/cube#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
ASK {
    ?obs qb:dataSet/qb:structure/qb:component/qb:componentProperty ?dim .
    ?dim a qb:DimensionProperty ;
        qb:codeList ?list .
    ?list a skos:ConceptScheme .
    ?obs ?dim ?v .
    FILTER NOT EXISTS { ?v a skos:Concept ; skos:inScheme ?list }
}
""",
"""
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
PREFIX qb:      <http://purl.org/linked-data/cube#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
ASK {
    ?obs qb:dataSet/qb:structure/qb:component/qb:componentProperty ?dim .
    ?dim a qb:DimensionProperty ;
        qb:codeList ?list .
    ?list a qb:HierarchicalCodeList .
    ?obs ?dim ?v .
    FILTER NOT EXISTS { ?list qb:hierarchyRoot/<$p>* ?v }
}
""",
"""
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
PREFIX qb:      <http://purl.org/linked-data/cube#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
ASK {
    ?obs qb:dataSet/qb:structure/qb:component/qb:componentProperty ?dim .
    ?dim a qb:DimensionProperty ;
         qb:codeList ?list .
    ?list a qb:HierarchicalCodeList .
    ?obs ?dim ?v .
    FILTER NOT EXISTS { ?list qb:hierarchyRoot/(^<$p>)* ?v }
}
"""
]

for file in [filenameCare, filenamePopulation]:
    g = rdflib.Graph()

    try:
      resultCare = g.parse(filenameCare, format='ttl', )

      print("-"*20)
      print(file)

      for queryPosition, query in enumerate(ICqueries):
          print("IC-"+str(queryPosition + 1)+":", end=" ")
          try:
            for row in g.query(query):            
              print(row)
          except:
            print("error")
    except:
       print("File problem")

