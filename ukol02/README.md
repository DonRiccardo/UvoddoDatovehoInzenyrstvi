# Vytvárame datacube

[Podrobnosti o úlohe](https://skoda.projekty.ms.mff.cuni.cz/ndbi046/seminars/03-airflow.html#/1/1) 

## Systémové požiadavky

Python >= 3.8 <br>
na správne fungovanie je potrebné mať nainštalované knižnice, ktoré sú špecifikované v  súbore [requirements](https://github.com/DonRiccardo/UvoddoDatovehoInzenyrstvi/blob/a8505c3844c8d50baf3263ef17ddd06d5f999809/ukol02/airflow/requirements.txt)
. <br>
. <br>
.. good luck :D

## Inštalačné inštrukcie

1) naklonujte si repository
2) otvorte priečinok „ukol02/airflow/“
3) nainštalujte requirements ``` pip instal -r requirements.txt ```
4) spustite airflow podľa vašich možností
5) následne môžete spustiť môj DAG, ktorý má id: „data-cubes“

## Scripty
### /airflow/dags/UdDI_ukol_02.py

Hlavná časť úlohy. Je to zdrojový súbor DAG.

### /airflow/dags/my_programs/homework01population.py

Po spustení vygeneruje datacube do súboru „population.ttl“. Prednastavená cesta vygenerovaného súboru je „airflow/dags/". Dá sa zmeniť použitím parametru „output_path“ špecifikovným v DAG konfigurácii.

### /airflow/dags/my_programs/homework01care.py

Po spustení vygeneruje datacube do súboru „health_care.ttl“. Prednastavená cesta vygenerovaného súboru je „airflow/dags/". Dá sa zmeniť použitím parametru „output_path“ špecifikovným v DAG konfigurácii.

### /airflow/dags/my_programs/prepareCSV_file.py

Zo stiahnutých požadovaných súborov predpriraví dáta na ďaľšie spracovanie, teda na vytvorenie jednotlivých data cube.



## Licencia

[MIT](https://github.com/DonRiccardo/UvoddoDatovehoInzenyrstvi/blob/b1953fa50e8ee1b31bede76221603edd67cba507/ukol02/license.txt)

