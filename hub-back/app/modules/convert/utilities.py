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
	max_count = 1

	if config and 'data' in config and 'start' in config['data']:
		min_count = config['data']['start']+1
	if config and 'data' in config and 'end' in config['data']:
		max_count = config['data']['end']

	_csv = import_csv(source, min_count, max_count)

	results = []

	for row in range(min_count, max_count):

		""" START CONVERSION PROCESS """

		thing_id = None # "NAME"
		location_id = None
		data_stream_id = None


		data_stream_name = ""

		""" RESULT VALUE DEFINITIONS """
		result_name = ""
		result_description = ""
		restult_properties = {}
		observations = {}
		observed_properties = {}
		sensor = {}
		locations = []
	

		""" THING AND PROPERTIES """
		for field in config['Thing']['fields']:

			if field['type']== 'single':

				if field['mapped_to']== 'name':

					result_name = get_data_from_csv_row(_csv,field['value'],row)

					thing_id = result_name.lower()
					thing_id = thing_id.replace(" ", "_")


				if field['mapped_to']== 'description':
					result_description = get_data_from_csv_row(_csv,field['value'],row)

			elif field['type']== 'many':

				if field['mapped_to']== 'properties':

					for val in field['value']:
		
						for key, value in val.items():
							if value and isinstance(value,dict):
								restult_properties[key]= get_data_from_csv_row(_csv,value,row)
							else:
								restult_properties[key]= ""

		for location in config['Locations']:
			location_coordinates = []
			for field in location['fields']:
				
				location_name = ""
				location_description = ""
				if field['type']== 'single':

					if field['mapped_to']== 'name':
						location_name = get_data_from_csv_row(_csv,field['value'],row)
						location_id = result_name.lower()
						location_id = location_id.replace(" ", "_")

					if field['mapped_to']== 'description':
						location_description = get_data_from_csv_row(_csv,field['field_name'],row)

					if field['mapped_to']== 'location_long':
						location_coordinates.append(get_data_from_csv_row(_csv,field['value'],row))

					if field['mapped_to']== 'location_lat':
						location_coordinates.append(get_data_from_csv_row(_csv,field['value'],row))

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
											unit_of_measurement[key]= get_data_from_csv_row(_csv,i_value,row)
									else:
										unit_of_measurement[key]= ""

						""" DATA STREAMS -- OBSERVED PROPERTIES """
						if field['mapped_to']== 'ObservedProperties':
							observed_properties ={}

							for val in field['value']:
								for key, value in val.items():
									if value and isinstance(value,dict):
										for i_key, i_value in value.items():
											data_stream_id = "%s %s" %(result_name, get_data_from_csv_row(_csv,i_value,row))
											data_stream_id = data_stream_id.lower()
											data_stream_id = data_stream_id.replace(" ", "_")
											observed_properties[key]= get_data_from_csv_row(_csv,i_value,row)
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
											sensor[key]= get_data_from_csv_row(_csv,i_value,row)
									else:
										
										if key == 'metadata':
											for item in value:
												for i_key, i_value in item.items():
													sensor_metadata[i_key]= get_data_from_csv_row(_csv,i_value,row)
											sensor['metadata']=sensor_metadata
										else:
											sensor[key]= value

						""" DATA STREAMS -- OBSERVATIONS """
						if field['mapped_to']== 'Observations':
							observations = {}
							for val in field['value']:
								for key, value in val.items():

									if value and isinstance(value,dict):
										for i_key, i_value in value.items():
											observations[key]= get_data_from_csv_row(_csv,i_value,row)
									elif value and isinstance(value,list):

										time_string = ""
										for item in value:
											for i_key, i_value in item.items():
												if len(time_string) > 0:
													time_string+= " " + get_data_from_csv_row(_csv,i_value,row)
												else:
													time_string+= get_data_from_csv_row(_csv,i_value,row)

										date_time_obj = datetime.strptime(time_string, '%m/%d/%y %H:%M:%S')

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

	""" THING AND PROPERTIES """
	for field in config['Thing']['fields']:

		if field['type']== 'single':

			if field['mapped_to']== 'name':
				result_name = get_data_from_excel_cell(workbook, \
							field['sheet'], \
							field['value'])
				thing_id = result_name.lower()
				thing_id = thing_id.replace(" ", "_")

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
					location_id = result_name.lower()
					location_id = location_id.replace(" ", "_")

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

	""" DATA STREAM """

	for datastream in config['Datastreams']:
		datastream_name = ""
		datastream_description = ""
		datastream_observation_type = ""
		unit_of_measurement_name = ""
		unit_of_measurement_symbol = ""
		unit_of_measurement_definition = ""
		sensor_name = ""
		sensor_description = ""
		sensor_encoding_type = ""
		sensor_metadata = ""
		observerd_property_name = ""
		observerd_property_definition = ""
		observerd_property_description = ""
		observation_time = ""
		observation_result = ""
		for field in datastream['fields']:
			
			if field['type']== 'single':

				if field['mapped_to']== 'name':
					datastream_name = get_data_from_excel_cell(workbook, \
								field['sheet'], \
								field['value'])
					data_stream_id = "%s %s" % (datastream_name.lower(), "param")
					data_stream_id = data_stream_id.replace(" ", "_")

				# datastream_observation_type = get_data_from_sheet_or_input('datastream_observation_type', field, workbook)

				if field['mapped_to']== 'datastream_observation_type':
					datastream_observation_type = get_data_from_sheet_or_input('datastream_observation_type', field, workbook)

				if field['mapped_to']== 'unit_of_measurement_symbol':
					unit_of_measurement_symbol = get_data_from_sheet_or_input('unit_of_measurement_symbol', field, workbook)

				if field['mapped_to']== 'unit_of_measurement_name':
					unit_of_measurement_name = get_data_from_sheet_or_input('unit_of_measurement_name', field, workbook)

				if field['mapped_to']== 'unit_of_measurement_definition':
					unit_of_measurement_definition = get_data_from_sheet_or_input('unit_of_measurement_definition', field, workbook)

				if field['mapped_to']== 'sensor_name':
					sensor_name = get_data_from_sheet_or_input('sensor_name', field, workbook)

				if field['mapped_to']== 'sensor_description':
					sensor_description = get_data_from_sheet_or_input('sensor_description', field, workbook)

				if field['mapped_to']== 'sensor_encoding_type':
					sensor_encoding_type = get_data_from_sheet_or_input('sensor_encoding_type', field, workbook)

				if field['mapped_to']== 'sensor_metadata':
					sensor_metadata = get_data_from_sheet_or_input('sensor_metadata', field, workbook)
					
				if field['mapped_to']== 'observerd_property_name':
					observerd_property_name = get_data_from_sheet_or_input('observerd_property_name', field, workbook)

				if field['mapped_to']== 'observerd_property_definition':
					observerd_property_definition = get_data_from_sheet_or_input('observerd_property_definition', field, workbook)

				if field['mapped_to']== 'observerd_property_description':
					observerd_property_description = get_data_from_sheet_or_input('observerd_property_description', field, workbook)

				if field['mapped_to']== 'observation_result':
					observation_result = get_data_from_sheet_or_input('observation_result', field, workbook)

				if field['mapped_to']== 'observation_time':
					if field['value_type']== 'input':
						observation_time = field['value']
					if field['value_type']== 'sheet':
						observation_time = get_data_from_excel_cell(workbook, \
								field['sheet'], \
								field['value'])
						observation_time = observation_time.isoformat()

		data_streams.append({
				"@iot.id":data_stream_id,
				"name": datastream_name,
				"description": datastream_description,
				"observationType": datastream_observation_type,
					"unitOfMeasurement": {
					"name": unit_of_measurement_name,
					"symbol": unit_of_measurement_symbol,
					"definition": unit_of_measurement_definition
				},
				"Sensor": {
					"name": sensor_name,
					"description": sensor_description,
					"encodingType": sensor_encoding_type,
					"metadata": sensor_metadata
				},
				"ObservedProperty": {
					"name": observerd_property_name,
					"definition": observerd_property_definition,
					"description": observerd_property_description
				},
				"Observations": [
					{
						"phenomenonTime": observation_time,
						"result":observation_result
					}
				]
			},)

						
	# """ MULTI DATA STREAMS """

	# for _data_stream in config['MultiDatastreams']:
	# 	for field in _data_stream['fields']:

	# 		if field['type']== 'single':
	# 			pass

	# 		if field['type']== 'many':

	# 			""" MULTI DATA STREAMS -- UNIT OF MEASUREMENTS """
	# 			if field['mapped_to']== 'unitOfMeasurements':
	# 				unit_of_measurements =[]

	# 				for val in field['value']:
	# 					_results_units = {}
	# 					for key, value in val.items():
	# 						_results_units[key]=value
	# 					unit_of_measurements.append(_results_units)

	# 			""" MULTI DATA STREAMS -- SENSOR """
	# 			if field['mapped_to']== 'Sensor':
	# 				sensor = {}
	# 				for val in field['value']:
	# 					for key, value in val.items():
	# 						sensor[key] = value

	# 			""" MULTI DATA STREAMS -- OBSERVED PROPERTY """
	# 			if field['mapped_to']== 'ObservedProperties':
	# 				observations = []
	# 				for val in field['value']:
	# 					observations.append({
	# 						'name':get_data_from_excel_cell(workbook, field['sheet'], val['name']),
	# 						'definition':val['definition'],
	# 						'description':val['description'],
	# 					})

	# 			""" MULTI DATA STREAMS -- OBSERVED PROPERTY """
	# 			if field['mapped_to']== 'Observations':
	# 				observations = get_observations(workbook, field['sheet'], field['value'])

	# 			#TODO Make this dynamic
	# 			""" OBSERVED PROPERTIES """
	# 			observed_properties = [
	# 				{
	# 					"name": "Depth to Water",
	# 					"definition": "",
	# 					"description": "feet below ground surface"
	# 				},
	# 				{
	# 					"name": "Groundwater Elevation",
	# 					"definition": "",
	# 					"description": "feet mean sea level"
	# 				}
	# 			]

	result = {
		"name": result_name,
		"description": result_description,
		"properties": restult_properties,
		"Locations": locations,
		"@iot.id": thing_id,
		"Datastreams": data_streams
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

			result = {"features":convert_data_from_csv(source,config)}


	return result


def create_config(config):

	result = {}

	return config



