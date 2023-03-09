# Vytvárame datacube

## Systémové požiadavky

Python >= 3.8 <br>
. <br>
. <br>
.. ? good luck :D

## Inštalačné inštrukcie

...

## Príprava dát

V priečinku „prepare_data“ sa nachádza jupyter notebook, pomocou ktorého som si pripravil dáta na požadovaný formát s danými hodnotami. 
Na prípravu dát som použil súbory s príponou „.csv“, ktoré sa nachádzaju v priečinku „./ukol01/“.
Výsledné súbory sú „preparedNRPZS.csv“ a „preparedMeanPocet.csv“.

## Scripty
### homework01population.py

Vygeneruje datacube do súboru „populationRDF.ttl“.


### homework01care.py

Vygeneruje datacube do súboru „careRDF.ttl“.

### homework01integrity.py

Overí integritu vygenerovaných datacube na základe dotazovania. Výsledky testov sú rozdelené pre jednotlivé súbory a vypísané do terminálu.
