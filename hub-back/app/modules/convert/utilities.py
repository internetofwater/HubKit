#!/usr/bin/env python

"""Convert Utilities package.

For license and copyright information please see the LICENSE document (the
"License") included with this software package. This file may not be used
in any manner except in compliance with the License unless required by
applicable law or agreed to in writing, software distributed under the
License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.
"""

from flask import abort
from flask import request
from flask import json
from flask import make_response
from flask import jsonify
from flask import current_app

import os

import os.path
import json

import urllib3
import csv
import pytz
import datetime

import requests
import time

import csv

from datetime import datetime
from datetime import timezone

from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException
from openpyxl import Workbook

from openpyxl.utils.cell import coordinate_from_string, column_index_from_string


from flask import current_app

def get_data_from_csv_row(csv,field_name,row):

	result = csv[row][field_name]

	return result

def import_csv(source):
	"""Import a comma separated document into the Clean Water Hub API.

	:param (object) self
		the current class (i.e., Application)

	@return (object) response
		the fully qualified response object
	"""
	result = []

	with open(source) as f:
		reader = csv.DictReader(f, delimiter=',')
		count = sum(1 for _ in reader)
		f.seek(0)
		reader = csv.DictReader(f, delimiter=',')
		for line in reader:
			result.append(line)
						
	return result

def convert_data_from_csv(source,config):
	""" START CONVERSION PROCESS """

	thing_id = ""
	location_id = ""
	data_stream_id = ""

	""" RESULT VALUE DEFINITIONS """
	result_name = ""
	result_description = ""
	restult_properties = {}
	data_streams = []
	observations = []
	observed_properties = []
	sensor = {}
	unit_of_measurements =[]
	locations = []


	output = []
	datasstreams = []
	error_log = []
	# GET NAME OF COLUMN

	# REPEAT FOR EVERY ROW IN THE SHEET


	_csv = import_csv(source)

	
	thing_name_value = config['settings']['thing_name_column']
	thing_description_value = config['settings']['thing_description_column']
	thing_lng_value = config['settings']['thing_lng_column']
	thing_lat_value = config['settings']['thing_lat_column']

	
	print("thing name", thing_name_value)
	for i in range(0, len(_csv)):
		thing_name =  "%s" % (get_data_from_csv_row(_csv,thing_name_value,i))
		thing_description =  "%s" % (get_data_from_csv_row(_csv,thing_description_value,i))
		lng =  "%s" % (get_data_from_csv_row(_csv,thing_lng_value,i))
		lat =  "%s" % (get_data_from_csv_row(_csv,thing_lat_value,i))
		
		thing_id = thing_name.lower()
		thing_id = thing_id.replace(" ", "_")

		parameters = []


		for param in config['parameters']:
			observation_type = param['observation_type'].strip()
			property_definition = param['property_definition'].strip()
			property_description = param['property_description'].strip()
			property_name = param['property_name'].strip()
			sensor_description = param['sensor_description'].strip()
			sensor_encoding_type = param['sensor_encoding_type'].strip()
			sensor_metadata = param['sensor_metadata'].strip()
			sensor_name = param['sensor_name'].strip()
			unit_definition = param['unit_definition'].strip()
			unit_name = param['unit_name'].strip()
			unit_symbol = param['unit_symbol'].strip()

			datastrem_id = "%s_%s" % (thing_id,property_name.lower())
			datastrem_id = datastrem_id.replace(" ", "_")

			parameters.append({
				"name":thing_name,
				"description":thing_description,
				"@iot.id":datastrem_id,
				"observation_type":observation_type,
				"property_definition":property_definition,
				"property_description":property_description,
				"property_name":property_name,
				"sensor_description":sensor_description,
				"sensor_encoding_type":sensor_encoding_type,
				"sensor_metadata":sensor_metadata,
				"sensor_name":sensor_name,
				"unit_definition":unit_definition,
				"unit_name":unit_name,
				"unit_symbol":unit_symbol
			})

		for datastream in config['datastreams']:
			data_stream_property_name = datastream['name'].strip()

			data_stream_iotid = "%s_%s" % (thing_id,data_stream_property_name.lower())
			data_stream_iotid = data_stream_iotid.replace(" ", "_")
			data_stream_phenomenonTime = datastream['phenomenonTime'].strip()
			data_stream_result = datastream['result'].strip()

			data_stream_phenomenonTime = "%s" % (get_data_from_csv_row(_csv,data_stream_phenomenonTime,i)).strip()
			data_stream_result = "%s" % (get_data_from_csv_row(_csv,data_stream_result,i))

			if data_stream_result is not None:

				if isinstance(data_stream_phenomenonTime, datetime):
			
					datasstreams.append({
						"@iot.id":data_stream_iotid,
						"phenomenonTime":data_stream_phenomenonTime.isoformat(),
						"result":data_stream_result
					})
				else: 
					try:
						date_time_obj = datetime.strptime(data_stream_phenomenonTime, '%d/%m/%Y')
						datasstreams.append({
						"@iot.id":data_stream_iotid,
						"phenomenonTime":date_time_obj.isoformat(),
						"result":data_stream_result
					})
					except:
						error_log.append({
						"name":thing_name,
						"error": "PhenomenonTime is not in a date format",
						"property":data_stream_property_name,
						"@iot.id":data_stream_iotid,
						"phenomenonTime":str(data_stream_phenomenonTime),
						"result":data_stream_result
					})
					
		

		output.append({
			"@iot.id":thing_id,
			"name": thing_name,
			"description": thing_description if thing_description else "none",
			"properties": {
			},
			"lng":lng,
			"lat":lat,
			"parameters":parameters
		})

	result = {
		"status":"okay yo yo",
		"output":output,
		"datatstreams":datasstreams,
		"error_log":error_log
	}

	create_data_file_to_import(config,result)

	return result
	

def import_excel(source):

	try:
		workbook = load_workbook(filename=source)
		sheet = workbook.active
		return workbook
		
	except InvalidFileException as error:
		error_response = str(error)
		abort(make_response(jsonify(message=error_response), 400))
		return None	

def import_json(config):

	try:
		data = json.load(open(config))
		return data
	except FileNotFoundError as error:
		error_response = str(error)
		abort(make_response(jsonify(message=error_response), 400))
		return None
    
def get_data_from_excel_cell(workbook, sheet,cell):

	_sheet_reference = sheet
	_cell_reference = cell

	sheet = workbook[_sheet_reference]
	_cell = sheet[_cell_reference]

	return _cell.value

def convert_date(date):
	result = None

	if date:
		result = date

	return result.isoformat()

def get_observations(workbook,sheet,model):
	result = []
	

	for item in model:

		start = item['start']
		end = item['end']
		for i in range(start,end):

			# TODO abstract the results 0 and 1
			# TODO abstract the params
			_date = convert_date(get_data_from_excel_cell(workbook, sheet, "%s%s" % (item['phenomenonTime'],i)))
			result.append({
						
						"phenomenonTime": _date,
						"result": [
							get_data_from_excel_cell(workbook, sheet, "%s%s" % (item['result'][0],i)), 
							get_data_from_excel_cell(workbook, sheet, "%s%s" % (item['result'][1],i))
						],
						"parameters":{
							"measured_by": get_data_from_excel_cell(workbook, sheet, "%s%s" % (item['parameters']['measured_by'],i)),
							"pump": "F%s" % get_data_from_excel_cell(workbook, sheet, "%s%s" % (item['parameters']['pump'],i)),
							"comments":"G%s" % get_data_from_excel_cell(workbook, sheet, "%s%s" % (item['parameters']['comments'],i))
						}
					})
	return result

def get_data_from_sheet_or_input(mapped_to, field, workbook):
	result = ""

	if field['value_type']== 'input':
		result = field['value']
	if field['value_type']== 'sheet':
		result = get_data_from_excel_cell(workbook, \
				field['sheet'], \
				field['value'])
	return result

def convert_data_from_excel(source, config):
	""" START CONVERSION PROCESS """

	thing_id = ""
	location_id = ""
	data_stream_id = ""

	""" RESULT VALUE DEFINITIONS """
	result_name = ""
	result_description = ""
	restult_properties = {}
	data_streams = []
	observations = []
	observed_properties = []
	sensor = {}
	unit_of_measurements =[]
	locations = []

	## EXCEL CONVERTION PROCESS ##
	""" IMPORT EXECL FILE """
	workbook = import_excel(source)
	if workbook:
		sheet = workbook.active
	else:
		abort(make_response(jsonify(message='Could not import excel file'), 400))

		#Get the name

	output = []
	datasstreams = []
	error_log = []
	# GET NAME OF COLUMN

	# REPEAT FOR EVERY ROW IN THE SHEET

	sheet = config['settings']['sheet']

	sh = workbook[sheet]

	

	thing_name_value = config['settings']['thing_name_column']
	thing_description_value = config['settings']['thing_description_column']
	thing_lng_value = config['settings']['thing_lng_column']
	thing_lat_value = config['settings']['thing_lat_column']
	

	for i in range(2, sh.max_row):
		thing_name =  sh["%s%s" % (thing_name_value,i)].value
		thing_description = sh["%s%s" % (thing_description_value,i)].value
		lng = sh["%s%s" % (thing_lng_value,i)].value
		lat = sh["%s%s" % (thing_lat_value,i)].value
		thing_id = thing_name.lower()
		thing_id = thing_id.replace(" ", "_")

		parameters = []


		for param in config['parameters']:
			observation_type = param['observation_type'].strip()
			property_definition = param['property_definition'].strip()
			property_description = param['property_description'].strip()
			property_name = param['property_name'].strip()
			sensor_description = param['sensor_description'].strip()
			sensor_encoding_type = param['sensor_encoding_type'].strip()
			sensor_metadata = param['sensor_metadata'].strip()
			sensor_name = param['sensor_name'].strip()
			unit_definition = param['unit_definition'].strip()
			unit_name = param['unit_name'].strip()
			unit_symbol = param['unit_symbol'].strip()

			datastrem_id = "%s_%s" % (thing_id,property_name.lower())
			datastrem_id = datastrem_id.replace(" ", "_")

			parameters.append({
				"name":thing_name,
				"description":thing_description,
				"@iot.id":datastrem_id,
				"observation_type":observation_type,
				"property_definition":property_definition,
				"property_description":property_description,
				"property_name":property_name,
				"sensor_description":sensor_description,
				"sensor_encoding_type":sensor_encoding_type,
				"sensor_metadata":sensor_metadata,
				"sensor_name":sensor_name,
				"unit_definition":unit_definition,
				"unit_name":unit_name,
				"unit_symbol":unit_symbol
			})

		for datastream in config['datastreams']:
			data_stream_property_name = datastream['name'].strip()

			data_stream_iotid = "%s_%s" % (thing_id,data_stream_property_name.lower())
			data_stream_iotid = data_stream_iotid.replace(" ", "_")
			data_stream_phenomenonTime = datastream['phenomenonTime'].strip()
			data_stream_result = datastream['result'].strip()

			data_stream_phenomenonTime = sh["%s%s" % (data_stream_phenomenonTime,i)].value
			data_stream_result = sh["%s%s" % (data_stream_result,i)].value

			if data_stream_result is not None:
				if isinstance(data_stream_phenomenonTime, datetime):
			
					datasstreams.append({
						"@iot.id":data_stream_iotid,
						"phenomenonTime":data_stream_phenomenonTime.isoformat(),
						"result":data_stream_result
					})
				else:
					error_log.append({
						"name":thing_name,
						"error": "PhenomenonTime is not in a date format",
						"property":data_stream_property_name,
						"@iot.id":data_stream_iotid,
						"phenomenonTime":str(data_stream_phenomenonTime),
						"result":data_stream_result
					})
		

		output.append({
			"@iot.id":thing_id,
			"name": thing_name,
			"description": thing_description if thing_description else "none",
			"properties": {
			},
			"lng":lng,
			"lat":lat,
			"parameters":parameters
		})

	result = {
		"status":"okay",
		"output":output,
		"datatstreams":datasstreams,
		"error_log":error_log
	}

	create_data_file_to_import(config,result)

	return result

def convert_data(source, config):


	basepath = current_app.config['MEDIA_BASE_PATH'] + 'files/'
	directory = os.getcwd() + '/app/static/usercontent/' + 'files/'


	_source_type = None
	result = {}

	""" IMPORT JSON CONFIG FILE """
	config = import_json(directory+"/"+config)

	source = directory+source


	if config:
		pass
	else: 
		abort(make_response(jsonify(message='Could not import config file'), 400))

	""" DETECT DATA SOURCE FILE """
	if config:
		if 'settings' in config and 'type' in config['settings']:
			_source_type = config['settings']['type']

		if os.path.splitext(source)[1] == '.csv':
			_source_type = 'csv'
		elif os.path.splitext(source)[1] == '.xlsx':
			_source_type = 'excel' 
		else:
			abort(make_response(jsonify(message="File type must be .csv or .xlsx"), 400))
			
		if _source_type == 'excel':
			result = convert_data_from_excel(source, config)
		elif _source_type == 'csv':
			result = convert_data_from_csv(source,config)


	return result

def create_config(config):

	# Save JSON File
	basepath = current_app.config['MEDIA_BASE_PATH'] + 'files/'
	directory = os.getcwd() + '/app/static/usercontent/' + 'files/'

	"""
	Prepare the file for processing
	"""

	extension = "json"
	if config and 'settings' in config and 'file' in config['settings']:
		filename = config["settings"]["file"]
	else:
		filename = "config." + extension

	filepath = os.path.join(directory, filename)
	fileurl = os.path.join(basepath, filename)

	with open(filepath, 'w') as outfile:
		json.dump(config, outfile)

	return config

def create_data_file_to_import(config,data):

	# Save JSON File

	basepath = current_app.config['MEDIA_BASE_PATH'] + 'files/'
	directory = os.getcwd() + '/app/static/usercontent/' + 'files/'

	"""
	Prepare the file for processing
	"""

	extension = "json"
	if config and 'settings' in config and 'file' in config['settings']:
		filename = config["settings"]["file"]
		filename = os.path.splitext(filename)[0]+'_data_to_import.' + extension
	else:
		filename = "data_to_import." + extension

	filepath = os.path.join(directory, filename)
	fileurl = os.path.join(basepath, filename)

	with open(filepath, 'w') as outfile:
		json.dump(data, outfile)

	return data


def get_column_headers(source, file_type):

	result = {}
	sheets = []

	if file_type == "excel":

		
		sheet_number = 0

		workbook = import_excel(source)
		if workbook:
			sheet = workbook.active
		else:
			abort(make_response(jsonify(message='Could not import excel file'), 400))
		
		for item in workbook.sheetnames:
			sheet = workbook[item]

			list_with_values=[]
			for cell in sheet[1]:

				list_with_values.append(
					{
						'column': cell.column_letter,
						'row':cell.row,
						'value':cell.value
					}
				)

			sheets.append({
				'sheet':item,
				'sheet_number':sheet_number,
				'headers':list_with_values
			})
			sheet_number = sheet_number + 1


	elif file_type == "csv":

		_csv = import_csv(source)
		list_with_values=[]

		count = 1
		for item in _csv[0]:
			
			list_with_values.append(
					{
						'column': item,
						'row':count,
						'value':item
					}
				)
			count = count + 1
		
		sheets.append({
				'sheet':'csv',
				'sheet_number':0,
				'headers':list_with_values
			})


	result ={
			"status":"File Loaded",
			"type": "FeatureCollection",
			"features": sheets
	}
	return result


def process_data(data): 

	response = None


	if "output" in data:
		for item in data["output"]:
			print("Starting Thing")

			path = "http://devops_web_1:8080/FROST-Server/v1.1"
			thing = "Things('%s')" % item["@iot.id"]
			url_collection = "%s/Things" % (path)
			url_thing = "%s/%s" % (path, thing)


			## CHECK FOR EXISTANCE
			try:
				response = requests.get(url=url_thing,
					headers={
						"Content-Type": "application/json; charset=utf-8",
					})
				data_output = response.json()
			#         print('Response HTTP Response Body: {content}'.format(
			#             content=response.content))
			except requests.exceptions.RequestException:
				print('HTTP Request failed - Frost Server is not on')
			## END CHECK FOR EXISTANCE

			if response is None:
				 abort(make_response(jsonify(message="FROST SERVER IS NOT ONLINE"), 400))

			if response.status_code == 200:
				print("We Got it")
				continue
			elif response.status_code == 404:
				# CREATE THE THING
				print("Let's Make the THING")

				datastreams = []

				for param in item['parameters']:
					datastreams.append(
						{
						"@iot.id":param['@iot.id'],
						"name": item['name'],
						"description":item['description'],
						"observationType":param['observation_type'],
						"unitOfMeasurement": {
							"name": param['unit_name'],
							"symbol":param['unit_symbol'],
							"definition": param['unit_definition'],
						},
						"Sensor": {
							"name": param['sensor_name'],
							"description": param['sensor_description'],
							"encodingType": param['sensor_encoding_type'],
							"metadata": param['sensor_metadata'],
						},
						"ObservedProperty": {
							"name": param['property_name'],
							"definition": param['property_definition'],
							"description": param['property_description'],
						},			
					})

				data_to_post = {
					"@iot.id":item['@iot.id'],
					"name": item['name'],
					"description": item['description'],
					"Locations": [{
						"name":  item['name'],
						"description":  item['description'],
						"encodingType": "application/vnd.geo+json",
						"location": {
							"type": "Point",
							"coordinates": [item['lng'], item['lat']]
						}
					}],
					"Datastreams": datastreams
				}
				data_to_post = json.dumps(data_to_post)
				print("BOUT TO POST SOME DATA")
				try:
					response = requests.post(url=url_collection,
						headers={
							"Content-Type": "application/json; charset=utf-8",
						},
						data=data_to_post
            			)
					# data = response.json()

					# print('Response HTTP Response Body: {content}'.format(
					# 	content=response.content))
				except requests.exceptions.RequestException:
					print('HTTP Request failed')	


	print("#############################")
	print("#############################")
	print("#############################")
	print("######## FINISHED THAT PART ")
	print("#############################")
	print("#############################")

	time.sleep(1)

	print("datatstreams" in data)
	print(len(data['datatstreams']))

	if "datatstreams" in data:
		for item in data['datatstreams']:
			print("Starting Data Stream")

			path = "http://devops_web_1:8080/FROST-Server/v1.1"
			observation = "Datastreams('%s')/Observations" % item["@iot.id"]
			url_data_stream = "%s/%s" % (path, observation)


			print("Datastream",url_data_stream)

			## CHECK FOR EXISTANCE
			try:
				response_check = requests.get(url=url_data_stream,
					headers={
						"Content-Type": "application/json; charset=utf-8",
					})
				data_data_stream = response_check.json()
			#         print('Response HTTP Response Body: {content}'.format(
			#             content=response.content))
			except requests.exceptions.RequestException:
				print('HTTP Request failed - Frost Server is not on')
			## END CHECK FOR EXISTANCE

			data_to_post =   {
					"phenomenonTime": item["phenomenonTime"],
					"result": item["result"]
				}

			print(data_to_post)


			data_to_post = json.dumps(data_to_post)
			if response_check.status_code == 200:
				print("It Exists - lets go for it")

				try:
					response_to_post = requests.post(url=url_data_stream,
						headers={
							"Content-Type": "application/json; charset=utf-8",
						},
						data=data_to_post
            			)
					# data = response.json()

					# print('Response HTTP Response Body: {content}'.format(
					# 	content=response.content))
				except requests.exceptions.RequestException:
					print('HTTP Request failed')
				
			elif response_to_post.status_code == 404:
				continue


	result = {
		"staus":"okay",
		"output":data_output,
		"datastream":data_data_stream,
		}

	return result