
from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta

from my_programs.prepareCSV_file import prepareDataForProcessing
from my_programs.homework01care import mainCreateCareDataCube
from my_programs.homework01population import mainCreatePopulationDataCube

import requests

def downloadData (url, verifySSL = True):
	filename = url.split("/")[-1]
	response = requests.get(url, verify=verifySSL)
	open(filename, "wb").write(response.content)
	return filename

def fileAtSpecifiedPath (function, **param):
	path = param["dag_run"].conf.get("output_path", "airflow/dags/")
	function(path)


dag_args = {
	"email": ["airflowadmin@example.com"],
	"email_on_failure": False,
	"email_on_retry": False,
	"retries": 1,
	'retry_delay': timedelta(minutes=15)
}

with DAG(
	dag_id = "data-cubes",
	default_args = dag_args,
	start_date = datetime(2023, 3, 22),
	schedule = None,
	catchup=False,
	tags=["NDBI046"], 
) as dag:
	
	#PREPARE DATA

	prepareDataForProcessing = PythonOperator(
		task_id = "prepare_data_for_processing",
		python_callable = prepareDataForProcessing
	)

	#CARE PROVIDERS CZECH REPUBLIC

	getDataForCareProviders = PythonOperator(
		task_id = "get_care_providers_data",
		python_callable = downloadData,
		op_args = ["https://opendata.mzcr.cz/data/nrpzs/narodni-registr-poskytovatelu-zdravotnich-sluzeb.csv"]
	)

	createDataCubeForCareProviders = PythonOperator(
		task_id = "create_data_cube_care_providers",
		python_callable = fileAtSpecifiedPath,
		op_args = [ mainCreateCareDataCube]
	)





	#POPULATION 2021 CZECH REPUBLIC

	getDataForPopulation2021 = PythonOperator(
		task_id = "get_population_2021_data",
		python_callable = downloadData,
		op_args = ["https://www.czso.cz/documents/10180/184344914/130141-22data2021.csv"]
	)

	getCountryCodeListForPopulation2021 = PythonOperator(
		task_id ="get_country_codelist_data",
		python_callable = downloadData,
		op_args = ["https://skoda.projekty.ms.mff.cuni.cz/ndbi046/seminars/02/číselník-okresů-vazba-101-nadřízený.csv", False]
	)

	getCodeListCounty = PythonOperator(
		task_id = "get_codelist_county_data",
		python_callable = downloadData,
		op_args = ["https://data.mzcr.cz/distribuce/69/okresy.csv"]
	)

	getCodeListRegion = PythonOperator(
		task_id = "get_codelist_region_data",
		python_callable = downloadData,
		op_args = ["https://data.mzcr.cz/distribuce/68/kraje.csv"]
	)

	createDataCubeForPopulation = PythonOperator(
		task_id = "create_data_cube_population",
		python_callable = fileAtSpecifiedPath,
		op_args = [mainCreatePopulationDataCube]
	)



[getDataForCareProviders, getDataForPopulation2021, getCountryCodeListForPopulation2021, getCodeListCounty, getCodeListRegion] >> prepareDataForProcessing >> [createDataCubeForCareProviders, createDataCubeForPopulation]
