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

import urllib3
import csv
import pytz
import datetime

import csv

from datetime import datetime
from datetime import timezone

from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException
from openpyxl import Workbook


from flask import current_app

def get_data_from_csv_row(csv,field_name,row):

	result = csv[row][field_name]

	return result


def import_csv(source, min_count, max_count):
	"""Import a comma separated document into the Clean Water Hub API.

	:param (object) self
		the current class (i.e., Application)

	@return (object) response
		the fully qualified response object
	"""
	result = []

	with open(source, mode='r') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		line_count = min_count
		max_count = max_count
		for row in csv_reader:
			if line_count > max_count:
				break
			if line_count == 0:
				line_count += 1
			if line_count >= 1:
				result.append(row)
				line_count += 1
						
			
	

	return result

def convert_data_from_csv(source,config):

	min_count = 0
	max_count = 15

	_csv = import_csv(source, min_count, max_count)

	results = []

	for row in range(min_count, max_count):

		""" START CONVERSION PROCESS """

		thing_id = "SAGER8019"
		location_id = "SAGER8019"
		data_stream_id = "SAGER8019"
		data_stream_name = ""

		""" RESULT VALUE DEFINITIONS """
		result_name = ""
		result_description = ""
		restult_properties = {}
		multi_data_streams = []
		observations = {}
		observed_properties = {}
		sensor = {}
		locations = []
	

		""" THING AND PROPERTIES """
		for field in config['Thing']['fields']:

			if field['type']== 'single':

				if field['mapped_to']== 'name':

					result_name = get_data_from_csv_row(_csv,field['field_name'],row)


				if field['mapped_to']== 'description':
					result_description = get_data_from_csv_row(_csv,field['field_name'],row)

			elif field['type']== 'many':

				if field['mapped_to']== 'properties':

					for val in field['value']:
		
						for key, value in val.items():
							if value and isinstance(value,dict):
								restult_properties[key]= get_data_from_csv_row(_csv,key,row)
							else:
								restult_properties[key]= ""


			# TODO ARE THERE ANY PROPERTIES TO MAP?
			# if field['type']== 'many':
			# 	if field['mapped_to']== 'properties':
			# 		for val in field['value']:
			# 			for key, value in val.items():
			# 				key_result = get_data_from_excel_cell(workbook, \
			# 					field['sheet'], \
			# 					key)
			# 				value_result = get_data_from_excel_cell(workbook, \
			# 					field['sheet'], \
			# 					value)
			# 				restult_properties[key_result] = value_result

		# """ LOCATIONS """


		for location in config['Locations']:
			location_coordinates = []
			for field in location['fields']:
				location_name = ""
				location_description = ""
				if field['type']== 'single':

					if field['mapped_to']== 'name':
						location_name = get_data_from_csv_row(_csv,field['field_name'],row)

					if field['mapped_to']== 'description':
						location_description = get_data_from_csv_row(_csv,field['field_name'],row)

					if field['mapped_to']== 'location_long':
						location_coordinates.append(get_data_from_csv_row(_csv,field['field_name'],row))

					if field['mapped_to']== 'location_lat':
						location_coordinates.append(get_data_from_csv_row(_csv,field['field_name'],row))

			""" DATA STREAMS """

			for _data_stream in config['Datastreams']:
				for field in _data_stream['fields']:

					if field['type']== 'single':
						pass

					if field['type']== 'many':

						""" DATA STREAMS -- UNIT OF MEASUREMENTS """
						if field['mapped_to']== 'unitOfMeasurements':
							unit_of_measurement ={}

							for val in field['value']:
								for key, value in val.items():
									if value and isinstance(value,dict): 
										for i_key, i_value in value.items():
											unit_of_measurement[key]= get_data_from_csv_row(_csv,i_key,row)
									else:
										unit_of_measurement[key]= ""

						""" DATA STREAMS -- UNIT OF MEASUREMENTS """
						if field['mapped_to']== 'ObservedProperties':
							observed_properties ={}

							for val in field['value']:
								for key, value in val.items():
									if value and isinstance(value,dict):
										for i_key, i_value in value.items():
											observed_properties[key]= get_data_from_csv_row(_csv,i_key,row)
									else:
										observed_properties[key]= ""

						""" DATA STREAMS -- SENSOR """
						if field['mapped_to']== 'Sensor':
							sensor = {}
							sensor_metadata = {}
							for val in field['value']:
								for key, value in val.items():
									if value and isinstance(value,dict):
										for i_key, i_value in value.items():
											sensor[key]= get_data_from_csv_row(_csv,i_key,row)
									else:
										
										if key == 'metadata':
											for item in value:
												for i_key, i_value in item.items():
													sensor_metadata[i_key]= get_data_from_csv_row(_csv,i_key,row)
											sensor['metadata']=sensor_metadata
										else:
											sensor[key]= value

						""" DATA STREAMS -- OBSERVED PROPERTY """
						if field['mapped_to']== 'Observations':
							observations = {}
							for val in field['value']:
								for key, value in val.items():

									if value and isinstance(value,dict):
										for i_key, i_value in value.items():
											observations[key]= get_data_from_csv_row(_csv,i_key,row)
									elif value and isinstance(value,list):

										time_string = ""
										for item in value:
											for i_key, i_value in item.items():
												if len(time_string) > 0:
													time_string+= " " + get_data_from_csv_row(_csv,i_key,row)
												else:
													time_string+= get_data_from_csv_row(_csv,i_key,row)

										date_time_obj = datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S')

										observations[key] = date_time_obj.isoformat()
							
									else:
										observations[key]= value


					
		locations.append({
			"name": location_name,
			"description": location_description,
			"encodingType": "application/vnd.geo+json",
			"@iot.id": location_id,
			"location": {
				"type": "Point",
				"coordinates": location_coordinates
				}
		})
							
		

		results.append({
			"name": result_name,
			"description": result_description,
			"properties": restult_properties,
			"Locations": locations,
			"@iot.id": thing_id,
			"Datastreams": [
				{
					"@iot.id":data_stream_id,
					"name": data_stream_name,
					"description": "",
					"observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_ComplexObservation",
					"unitOfMeasurement": unit_of_measurement,
					"Sensor": sensor,
					"ObservedProperty": observed_properties,
					"Observations": [observations],
				}
			]
		})

	return results

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


    #  with open(filepath) as json_file:
    #         try:
    #             data = json.load(json_file)
    #         except:
    #             result = get_org_and_suborg_sites(id)
    #             with open(filepath, 'w') as json_file:
    #                 json.dump(result, json_file)
    #             with open(filepath) as json_file:
    #                     data = json.load(json_file)
    
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

def convert_data_from_excel(source, config):
	""" START CONVERSION PROCESS """

	thing_id = "SAGER8010"
	location_id = "SAGER8010"
	data_stream_id = "SAGER8010"

	""" RESULT VALUE DEFINITIONS """
	result_name = ""
	result_description = ""
	restult_properties = {}
	multi_data_streams = []
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

	""" THING AND PROPERTIES """
	for field in config['Thing']['fields']:

		if field['type']== 'single':

			if field['mapped_to']== 'name':
				result_name = get_data_from_excel_cell(workbook, \
							field['sheet'], \
							field['value'])

			if field['mapped_to']== 'properties':
				restult_properties = get_data_from_excel_cell(workbook, \
							field['sheet'], \
							field['value'])

			if field['mapped_to']== 'description':
				result_description = get_data_from_excel_cell(workbook, \
							field['sheet'], \
							field['value'])

		if field['type']== 'many':
			if field['mapped_to']== 'properties':
				for val in field['value']:
					for key, value in val.items():
						key_result = get_data_from_excel_cell(workbook, \
							field['sheet'], \
							key)
						value_result = get_data_from_excel_cell(workbook, \
							field['sheet'], \
							value)
						restult_properties[key_result] = value_result

	""" LOCATIONS """


	for location in config['Locations']:
		for field in location['fields']:
			location_name = ""
			location_description = ""
			location_coordinates = []
			if field['type']== 'single':

				if field['mapped_to']== 'name':
					location_name = get_data_from_excel_cell(workbook, \
								field['sheet'], \
								field['value'])

				if field['mapped_to']== 'description':
					location_description = get_data_from_excel_cell(workbook, \
								field['sheet'], \
								field['value'])

			if field['type']== 'many':
				if field['mapped_to']== 'location':
					for val in field['value']:
						location_coordinates.append(get_data_from_excel_cell(workbook, \
								field['sheet'], \
								val))
					locations.append({
						"name": location_name,
						"description": location_description,
						"encodingType": "application/vnd.geo+json",
						"@iot.id": location_id,
						"location": {
							"type": "Point",
							"coordinates": location_coordinates
							}
					})
						
	""" MULTI DATA STREAMS """

	for _data_stream in config['MultiDatastreams']:
		for field in _data_stream['fields']:

			if field['type']== 'single':
				pass

			if field['type']== 'many':

				""" MULTI DATA STREAMS -- UNIT OF MEASUREMENTS """
				if field['mapped_to']== 'unitOfMeasurements':
					unit_of_measurements =[]

					for val in field['value']:
						_results_units = {}
						for key, value in val.items():
							_results_units[key]=value
						unit_of_measurements.append(_results_units)

				""" MULTI DATA STREAMS -- SENSOR """
				if field['mapped_to']== 'Sensor':
					sensor = {}
					for val in field['value']:
						for key, value in val.items():
							sensor[key] = value

				""" MULTI DATA STREAMS -- OBSERVED PROPERTY """
				if field['mapped_to']== 'ObservedProperties':
					observations = []
					for val in field['value']:
						observations.append({
							'name':get_data_from_excel_cell(workbook, field['sheet'], val['name']),
							'definition':val['definition'],
							'description':val['description'],
						})

				""" MULTI DATA STREAMS -- OBSERVED PROPERTY """
				if field['mapped_to']== 'Observations':
					observations = get_observations(workbook, field['sheet'], field['value'])

				#TODO Make this dynamic
				""" OBSERVED PROPERTIES """
				observed_properties = [
					{
						"name": "Depth to Water",
						"definition": "",
						"description": "feet below ground surface"
					},
					{
						"name": "Groundwater Elevation",
						"definition": "",
						"description": "feet mean sea level"
					}
				]

	result = {
		"name": result_name,
		"description": result_description,
		"properties": restult_properties,
		"Locations": locations,
		"@iot.id": thing_id,
		"MultiDatastreams": [
			{
				"@iot.id":data_stream_id,
				"name": "Params",
				"description": "",
				"observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_ComplexObservation",
				"multiObservationDataTypes": [
					"http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
					"http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement"
				],
				"unitOfMeasurements": unit_of_measurements,
				"Sensor": sensor,
				"ObservedProperties": observed_properties,
				"Observations": observations,
			}
		]
	}

	return result

def convert_data(source, config):

	_source_type = None
	result = {}

	""" IMPORT JSON CONFIG FILE """
	config = import_json(config)

	if config:
		pass
	else: 
		abort(make_response(jsonify(message='Could not import config file'), 400))

	""" DETECT DATA SOURCE FILE """
	if config:
		if 'data' in config and 'type' in config['data']:
			_source_type = config['data']['type']

		if _source_type == 'excel':
			result = convert_data_from_excel(source, config)
		elif _source_type == 'csv':
			# result = convert_data_from_excel(source, config)
			result = {"features":convert_data_from_csv(source,config)}


	return result



