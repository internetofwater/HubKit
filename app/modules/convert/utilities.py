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

from datetime import datetime
from datetime import timezone

from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

from flask import current_app


def import_csv(source):
    """Import a comma separated document into the Clean Water Hub API.

    :param (object) self
        the current class (i.e., Application)

    @return (object) response
        the fully qualified response object
    """
    logger.info('Application started to import data, %s, %s',
                source)

    """Open the CSV from source filepath provided.
    """
    try:
        response = urllib3.urlopen(source)
        reader = csv.reader(response)
    except urllib2.HTTPError as error:
        logger.error('Invalid path provided, please make sure you are \
                        prepending the appropriate file:/// or http:// \
                        prefix to the URL')
        reader = error.read()

    """Process each row of the CSV saving each row as a separate Feature.
    """
    for index, row in enumerate(reader):
        logger.info('Processing row data %d', index)

        """Skip the header row.
        """
        if index > 0:
            self.csv_row_to_json(row)

    """ImportData completed successfully.
    """
    logger.info('ImportData completed at %s', datetime.utcnow())

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
			break

	return result

def convert_data(source, config):

	""" IMPORT EXECL FILE """
	workbook = import_excel(source)
	if workbook:
		sheet = workbook.active
	else:
		abort(make_response(jsonify(message='Could not import excel file'), 400))


	""" IMPORT JSON CONFIG FILE """
	config = import_json(config)

	if config:
		pass
	else: 
		abort(make_response(jsonify(message='Could not import config file'), 400))


	""" START CONVERSION PROCESS """

	thing_id = "SAGER6792"
	location_id = "SAGER6792"

	""" THING AND PROPERTIES """

	result_name = ""
	result_description = ""
	restult_properties = {}

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
	locations = []

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
	multi_data_streams = []
	observations = []
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

	

	result = {
		"name": result_name,
		"description": result_description,
		"properties": restult_properties,
		"Locations": locations,
		"@iot.id": thing_id,
		"MultiDatastreams": [
			{
				"name": "Params",
				"description": "",
				"observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_ComplexObservation",
				"multiObservationDataTypes": [
					"http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
					"http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement"
				],
				"unitOfMeasurements": unit_of_measurements,
				"Sensor": sensor,
				"ObservedProperties": [
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
				],
				"Observations": observations,
			}
		]
	}


	return result



