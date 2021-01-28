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
    except InvalidFileException as error:
        error_response = str(error)
        abort(make_response(jsonify(message=error_response), 400))

def import_json(config):

    try:
        data = json.load(open(config))
        print(data)
    except FileNotFoundError as error:
        error_response = str(error)
        abort(make_response(jsonify(message=error_response), 400))


    #  with open(filepath) as json_file:
    #         try:
    #             data = json.load(json_file)
    #         except:
    #             result = get_org_and_suborg_sites(id)
    #             with open(filepath, 'w') as json_file:
    #                 json.dump(result, json_file)
    #             with open(filepath) as json_file:
    #                     data = json.load(json_file)
    


def convert_data(source, config):

    """ IMPORT EXECL FILE """
    import_excel(source)

    """ IMPORT EXECL FILE """
    import_json(config)


    result = {
	"name": "Piezometer - Deep",
	"description": "",
	"properties": {
		"aquifer": "Artesian",
		"total_depth": "529",
		"well_number": "none",
		"public_land_survey_system":"20.25.12.442"
	},
	"Locations": [
		{
			"name": "Piezometer - Deep",
			"description": "",
			"encodingType": "application/vnd.geo+json",
			"location": {
				"type": "Point",
				"coordinates": [32.583920, 104.430730]
			}
		}
	],
	"MultiDatastreams": [
		{
			"name": "Params",
			"description": "",
			"observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_ComplexObservation",
			"multiObservationDataTypes": [
				"http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
				"http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement"
			],
			"unitOfMeasurements": [
				{
					"name": "ft",
					"symbol": "ft",
					"definition": "ucum:ft_i"
				},
				{
					"name": "ft",
					"symbol": "ft",
					"definition": "ucum:ft_i"
				}
			],
			"Sensor": {
				"name": "Steel Tape",
				"description": "Measured by a human with a steel tape",
				"encodingType": "text",
				"metadata": ""
			},
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
			"Observations": [
				{
					"phenomenonTime": "2006-08-29T18:13:00Z",
					"result": [49.08, 3274.9],
					"parameters":{
						"measured_by": "ANEC-HRC",
						"pump": "NONE",
						"comments":"Depth from steel tape"
					}
				},
				{
					"phenomenonTime": "2006-09-18T09:04:00Z",
					"result": [45.13, 3278.9],
					"parameters":{
						"measured_by": "ANEC-HRC",
						"pump": "NONE",
						"comments":""
					}
				},
				{
					"phenomenonTime": "2006-10-23T11:04:00Z",
					"result": [49.08, 3274.9],
					"parameters":{
						"measured_by": "ANEC-HRC",
						"pump": "NONE",
						"comments":""
					}
				}
			]
		}
	]
}


    return result



