# Vytvárame datacube

[Podrobnosti o úlohe](https://skoda.projekty.ms.mff.cuni.cz/ndbi046/seminars/02-data-cube.html#/3) 

## Systémové požiadavky

Python >= 3.8 <br>
na správne fungovanie je potrebné mať nainštalované knižnice, ktoré sú špecifikované v  súbore [requirements](https://github.com/DonRiccardo/UvoddoDatovehoInzenyrstvi/blob/21484ed39bf7e23c3ea61a0c6a8e80ad799b5a35/ukol01/requirements.txt)
. <br>
. <br>
.. good luck :D

## Inštalačné inštrukcie

1) naklonujte si repository
2) otvorte priečinok „ukol01/“
3) nainštalujte requirements ``` pip instal -r requirements.txt ```
4) spustite požadovaný kód, napr. : ``` python homework01integrity.py```

## Ako som pripravil dáta

V priečinku „./prepare_data/“ sa nachádza jupyter notebook, pomocou ktorého som pripravil dáta na požadovaný formát s danými hodnotami. 
Na prípravu dát som použil súbory s príponou „.csv“, ktoré sa nachádzaju v priečinku „./ukol01/“.
Výsledné súbory sú „preparedNRPZS.csv“ a „preparedMeanPocet.csv“. <br>


## Scripty
### homework01population.py

Po spustení vygeneruje datacube do súboru „populationRDF.ttl“.


### homework01care.py

Po spustení ygeneruje datacube do súboru „careRDF.ttl“.

### homework01integrity.py

Po spustení overí integritu vygenerovaných datacube na základe dotazovania. Výsledky testov sú rozdelené pre jednotlivé súbory a vypísané do terminálu.



## Licencia

[MIT](https://github.com/DonRiccardo/UdDI/blob/d0291e5a83fc1bfcafb95b48fe7b241e13cc254d/ukol01/license.txt)
