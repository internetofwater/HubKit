- [HubKit Introduction](#hubkit-introduction)
- [Installation](#installation)
  * [Prerequisites](#prerequisites)
  * [Local Testing](#local-testing)
  * [Production (on the web with a domain name and password protection)](#production--on-the-web-with-a-domain-name-and-password-protection-)
    + [Configure domain name](#configure-domain-name)
    + [Change the password](#change-the-password)
- [Using](#using)
  * [Configuring CSVs](#configuring-csvs)
    + [Requirements for CSV format](#requirements-for-csv-format)
    + [Using the GUI](#using-the-gui)
  * [Scheduling automatic updates](#scheduling-automatic-updates)

# HubKit Introduction

HubKit is modular collection of services that would allow providers of time-series sensor data to (completed aspects marked, planned aspects unmarked)

1. [x] 1. Use a graphical user interface (GUI) to map their data in .csv files to a SensorThings API data model
1. [x] 2. Use the GUI to upload local sensor data .csv files to a SensorThings API endpoint
1. [x] 3. Use the GUI to schedule the uploading of sensor data from remote/ online .csv files at a regular interval to a SensorThings API endpoint
1. [x] 4. Serve data to the public (or authorized users) using the SensorThings API endpoint
1. [ ] 5. Publish sensor-specific landing pages with embedded [JSON-LD](https://json-ld.org), to comport with guidance for participating in the Internet of Water [geoconnex.us](https://geoconnex.us) system
1. [ ] 6. Serve data to the public and allow data downloads through a map-based GUI


The diagram below shows the different software elements of HubKit:




# Installation

## Prerequisites

The easiest way to install HubKit is to use our Docker images and `docker-compose`. In this way, the only prerequisite is a server with Docker and docker-compose installed. 

* [Instructions to install Docker and docker-compose on Mac or Windows Desktop environments](https://docs.docker.com/get-docker/)
* Instructions to install Docker on a Linux server: [(see "Installation per Distro" for instructions depending on which Linux version)](https://docs.docker.com/engine/install/)
* [Instructions to install docker-compose](https://docs.docker.com/compose/install/)

If working on Linux, you may want to follow the [post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/) as well to make sure you can run docker commands with your user pemissions on your machine.

You can copy all of the source code for the repository for local development in a local directory. Clone this repository, i.e.

`git clone https://github.com/internetofwater/HubKit.git`

You may have to [install git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), if it is not installed on your machine

## Local Testing

1. Open a terminal (Linux/Mac) / powershell (Windows) window
2. Type and enter `cd <your directory of choice>` This step determines which folder on your computer the software will be downloaded to
3. `git clone httpe://github.com/internetofwater/HubKit.git` This step downloads the source code as well as special code to run the software to the folder in step 2.
4. `cd HubKit/delpoy/local` This navigates to the folder where the code to run the software is. This code is the file `docker-compose.yml`, which you can see [here](https://github.com/internetofwater/HubKit/blob/main/deploy/local/docker-compose.yml)
5. `docker-compose up -d` This command runs `docker-compose.yml`, which will deploy the software.
    - If you see an error about permissions, you may need to run `sudo docker-compose up -d`
6. After a few minutes, the program will be running. You can check that software is running with the command `docker logs webapp`. When the system is ready to use, the response should end in a log in the terminal window like this: `✔ Compiled successfully.` The webapp (GUI) will be available to use to map and upload csv files by opening any web browser and navigating to http://localhost:4200. The SensorThings API endpoint will be available at http://localhost:8080/FROST-Server/v1.1



## Production (on the web with a domain name and password protection)

To deploy HubKit so that is available on the internet, you should have a server that is open to https traffic. This might be server on your own premises or a virtual machine provided by your IT office or a virtual machine you manage yourself from a public cloud provider such as Amazon Web Services, Google Cloud Platform, Microsoft Azure, or Digital Ocean. For steps on setting up virtual machines with one of these providers, see

- [Amazon Web Services EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html)
- [Google Cloud Platform Compute Engine](https://codelabs.developers.google.com/codelabs/cloud-compute-engine#0)
- [Microsoft Azure](https://docs.microsoft.com/en-us/learn/modules/create-linux-virtual-machine-in-azure/)
- [Digital Ocean Droplet](https://docs.digitalocean.com/products/droplets/how-to/create/)

It is reccomended to have a machine with at least 4GB of RAM.

### Configure domain name

HubKit includes a webserver that provides SSL certificates automatically, so that users have a secure connection. Thus, it is required to provide a domain name (e.g. yourdomain.com) . If you don't have a domain name, you can purchase one from domain registrars such as: [Google Domains], [Route53], [Domain.com], [Namecheap], among others. Once you have a domain name, you can configure many subdomains (e.g. hubkit.yourdomain.com).

1. Find your web server's IP Address.
2. Create an "A" DNS record that points your desired subdomain (e.g., hubkit.youdomain.com) to the IP address 
3. Fork this repository in GitHub.
4. Modify the `docker-compose.yml` file, changing "yourdomain.com" to the desired subdomain you registered in the code block below. Depending his can be done with command line tools like [vi](https://en.wikipedia.org/wiki/Vi) or [nano](https://www.nano-editor.org/dist/latest/nano.html).
```
    caddy: 
        image: caddy:2.4.6-alpine
        container_name: webserver
        environment:
          - DOMAIN=yourdomain.com #change to your domain
```
5. Modify the `docker-compose.yml` file, changing "http://localhost:8080/FROST-Server" to "https://{your subdomain}/api" in the code block below. Note the change from `http` to `https` and the change from `FROST-Server` to `api`.
```
 web:
        container_name: frost
        image: fraunhoferiosb/frost-server:latest
        environment:
            - serviceRootUrl=http://localhost:8080/FROST-Server #change to desired URL for production
            - http_cors_enable=true
```
6. Modify the `docker-compose.yml` file, changing the FROST username and password settings to values of your choice:

<img width="1045" alt="image" src="https://user-images.githubusercontent.com/44071350/160005612-91dd2de6-b45f-43ad-adf6-3e41e72c6f21.png">


7. Ensure that your VM allows connections over http and https (ports 80 and 443)
8. log in to your VM
9. Install Docker and git on your VM
10. `git clone https://github.com/{your github name}/HubKit`
11. `cd HubKit/deploy/web`
12. `docker-compose up -d` or if necessary, `sudo docker-compose up -d`

After a few minutes, the CSV configurator GUI will be available at https://yoursubdomain.yourdomain.com and the SensorThings API endpoint will be available at https://yoursubdomain.yourdomain.com/api/v1.1

The default username is `hubkit` and the default password is `ChangeMe`

### Change the password

Of course, additional levels of security may be desirable. This may move onto our roadmap in the future. For now, additional security must be configured in a custom manner. HubKit supports [basicauth as configurable in Caddy](https://caddyserver.com/docs/caddyfile/directives/basicauth).

To change the password from the defaults, you can change the Caddyfile within the `webserver` docker container. The default Caddyfile has two code blocks involving authentication:

```
   basicauth @api {
         hubkit JDJhJDE0JFA5bXRCQ1VCTVM1bUF6bzJRVTdKaC5BalE4V2pUL1RxZEJtTlREOXRROFlCNE9uNEI2YTVx #change as appropriate
    }
    basicauth @ui {
         hubkit JDJhJDE0JFA5bXRCQ1VCTVM1bUF6bzJRVTdKaC5BalE4V2pUL1RxZEJtTlREOXRROFlCNE9uNEI2YTVx #change as appropriate
    }

```

The `@api` block sets the password required to edit data using the SensorThings API. By default, reading (HTTP GET verbs) are open for the SensorThings API. The `@ui` block sets the password required to interact with the CSV configurator user interface. To change the password, edit these blocks, replacing `hubkit` with your desired username for each block, and replacing the long string beginning `JDJ` with a bcrypt password hash. 

  Change `hubkit` to what you would like the username to be. Change `JDJhJDE0JFA5bXRCQ1VCTVM1bUF6bzJRVTdKaC5BalE4V2pUL1RxZEJtTlREOXRROFlCNE9uNEI2YTVx` to the hash of your desired password. To create a password hash, a simple command to run from within your server is
  
  `docker run caddy caddy hash-password --plaintext {your password}`. 
  
  For example, `docker run caddy caddy hash-password --plaintext ChangeMe` results in `JDJhJDE0JG5ZYzg3cUZQNm5kMDZYbjRFb3A5eGVnL0ZjbmwyclhTMVNERlhTcFBxVVRKZ0xaM25HM1Jp`.
  
 

# Using
## Configuring CSVs

### Requirements for CSV format
The GUI is designed to work with CSV files with a ["tidy" data structure](https://vita.had.co.nz/papers/tidy-data.pdf), meaning every column is a variable, and every row is an observation. A sample minimum table is shown below:

| station_identifier| latitude | longitude| timestamp | variable1 | variable2 |
|-|-|-|-|-|-|
|station-1| 35.894 |-79.0314 |2022-03-28T01:00:00.000Z|10|15|
|station-1| 35.894 |-79.0314 |2022-03-28T01:15:00.000Z|11|14|
|station-2|35.9603| -78.9826|2022-03-28T01:00:00.000Z|2|7|
|station-2|35.9603| -78.9826|2022-03-28T01:15:00.000Z|3|5|

This data is also available as a csv file [here](https://raw.githubusercontent.com/internetofwater/HubKit/main/examples/data/example.csv).

The minimum required fields include:

1. A column that identifies a station/sensor/monitoring location
2. A column that identifies the latitude (WGS84) of the location (do note that every row must repeat this information. We will work on addressing this redundancy in the future)
3. A column that identifies the longitude (WGS84) of the location do note that every row must repeat this information. We will work on addressing this redundancy in the future)
4. A column indicating the date-time stamp in ISO 8061 format (YYYY-MM-DDTHH:MM:SS.sssZ) in the UTC timezone. We will be working to enable more customized data-time parsing in the the future.
5. A column for each variable that data is being collected on

The columns can have any name and be in any order. Multiple such CSV files can be configured. 

### Using the GUI

The GUI is located at your domain or at http://localhost:4200  if you are testing locally. The basic screen looks like this:

![image](https://user-images.githubusercontent.com/44071350/160647694-85f85f9b-7c0c-44c4-bc1a-990ed5d04d37.png)

The block "Load Configuration File" is for cases where you have already configured a CSV file, and would like to use a similar configuration for a new CSV file. To start from scratch, begin with the "Settings" block. You may choose either "Choose from File" to upload a CSV file from your computer, or "Choose from Web" to provide a URL. To try it out, you can use the sample data URL: https://raw.githubusercontent.com/internetofwater/HubKit/main/examples/data/example.csv

Click "Upload", then scroll down to "Select your data sheet source", and use the dropdown menus to select the csv, and then the columns to each of the required fields for name (which is the identifier for the station/location), description (which can be the same column, but can be a different column with a more detailed description), and latitude and longitude. 
<img width="998" alt="image" src="https://user-images.githubusercontent.com/44071350/160880988-fb2d6eec-1410-4751-aa99-9bc2c0a412ef.png">

Once this this is done, scroll down to "Add Your Parameters" to configure the adding of the actual observation data. Click "Add Parameter". From here you can configure the Observed Propery (parameter, variable, etc.), the units, and the Sensor (or Method) metadata associated with the column. Below is some guidance for each field:

* *Property Name*: A short name for the property (e.g. "groundwater depth", "gage height", "streamflow", "Total Dissovled Solids") Common names from from this vocabulary list are a good source. http://vocabulary.odm2.org/variablename/ 
* *Property Definition*: This could be a sentence. Ideally, it is a URL for a web page that defines the concept. For example, http://vocabulary.odm2.org/variablename/streamflow/
* *Property Description*: A longer description to clarify what the property is (e.g. for "streamflow", "The volume of water flowing past a fixed point over a fixed period of time") 
* *Observation Type*: A URI denoting what kind of observation values are to be expected (e.g. category, numeric, integer, free text). In general, should be one of the following:

|observationType| expected value types |
|-|-|
|http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_CategoryObservation | text/string or URI (e.g. "red" or "https://colors.com/red" |
|http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_CountObservation| integer |
|http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement | numeric |
|http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Observation| any |
|http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_TruthObservation | boolean (true/false)|

* *Unit of Measurement*: The name of the relevant units (e.g. "cubic feet per second")
* *Unit symbol*: The relevant symbol (e.g. "cfs")
* *Unit definition*: Either a sentence definition or a URI for one. For example, http://qudt.org/vocab/unit#CubicFootPerSecond
* *Sensor Name*: This should be an identifying name for either a particular sensor (e.g. "Stream Gage 1234") or a generalized type of sensor or method (e.g. "Stream gage" or "Chemical sample assay EPA method XYZ"). 
* *Sensor Description*: A more detailed description of the Sensor (e.g. "Stream gage at Station 1234" or "Chemical sample essay EPA method XYZ for copper, nickel, and lead")
* *Sensor Encoding type*: mimeTypes or other values to indicate what format any sensor metadata(see below) is in. "application/pdf" for a link to a PDF file, "text/html" for a website, "http://www.opengis.net/doc/IS/SensorML/2.0" for a SensorML XML document. (can be left blank if there is none)
* *Sensor Metadata*: A url pointing to a detailed description of the sensor (can be left blank if there is none).

*Result* is a dropdown for you to choos which column of the csv the relevant observation values are in.
*Data and Time* is a dropdown for you to choose which column of the csv the YYYY-MM-DDTHH:MM:SS.sssZ - formatted datetime values are in.

See below for a completed example:

<img width="966" alt="image" src="https://user-images.githubusercontent.com/44071350/160915163-d6603c01-dee3-47de-8e89-65ca473ca03d.png">

You can do this process again for other parameters/columns by clocking "Add Parameter" again. You can also edit the parameter by clicking the button that appears above "Add Parameter" corresponding to each parameter you have already added.

When you are finished adding parameters, click "Save". Then, in the top menu, click "Save Config". This will both save this configuration internally, and initiate a download of a document called "config.json" that looks like this:

```
{
    "datastreams": [
        {
            "id": 0,
            "name": "Streamflow",
            "phenomenonTime": "timestamp",
            "result": "variable1"
        }
    ],
    "parameters": [
        {
            "description": "",
            "id": "",
            "name": "",
            "observation_type": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
            "property_definition": "http://vocabulary.odm2.org/variablename/streamflow/",
            "property_description": "The volume of water flowing past a fixed point. Equivalent to discharge",
            "property_name": "Streamflow",
            "sensor_description": "A bubbler-based streamgage",
            "sensor_encoding_type": "pdf",
            "sensor_metadata": "https://pubs.usgs.gov/tm/tm3-a7/tm3a7.pdf",
            "sensor_name": "Streamgage",
            "unit_definition": "Volumetric flow rate",
            "unit_name": "Cubic feet per second",
            "unit_symbol": "http://qudt.org/vocab/unit#CubicFootPerSecond"
        }
    ],
    "settings": {
        "data_structure": "One Sensor per row",
        "file": "transform_config.json",
        "file_url": "https://raw.githubusercontent.com/internetofwater/HubKit/main/examples/data/example.csv",
        "sheet": "csv",
        "source": "example.csv",
        "thing_description_column": "﻿station_identifier",
        "thing_lat_column": "latitude",
        "thing_lng_column": "longitude",
        "thing_name_column": "﻿station_identifier",
        "type": "Excel"
    }
}
```

This tells HubKit exactly how to convert your CSV data into the SensorThings data model. You may want to rename and save config.json somewhere logical for safekeeping and reuse. Once config.json is saved, you can click "prep data for upload". If you scroll to the top, the red box will indicate if there are any errors in the CSV that need to be corrected. <img width="955" alt="image" src="https://user-images.githubusercontent.com/44071350/160916568-aa05e166-3af5-4673-8eba-bb627d9f6e21.png">

If there are no errors, click "Start Processing Data", which will upload the data. The data will then be available as a SensorThings API endpoint from {yourdomain.com}/api/v1.1 . An introduction for how to work with this endpoint can be found [here](https://fraunhoferiosb.github.io/FROST-Server/sensorthingsapi/3_GettingData.html). Some examples of working with the data in python can be found [here](https://github.com/BritishGeologicalSurvey/sensor-things-api-demo/blob/main/sensor-things-api-demo.ipynb)



## Scheduling automatic updates

HubKit allows for the use case of updating a CSV, and importing any new data in that CSV at a regular interval. As long as the CSV is available from a persistent HTTP(S) URL, this is possible. To configure this option, you msut first go through all the steps above. Once you have, you may click the "Schedule" button. Click "choose file" to load the config.json that you saved to your computer in the initial configuration step. Name the cron job, and specify the URL where your CSV is located, and select the time interval you want HubKit to look for new data in the CSV. Click "Schedule" when you are ready. An example scheduleer form is filled out below:

<img width="977" alt="image" src="https://user-images.githubusercontent.com/44071350/161107984-f35457b1-85bb-4974-9348-8c35edc267e9.png">





