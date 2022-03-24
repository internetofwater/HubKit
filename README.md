- [HubKit Introduction](#hubkit-introduction)
- [Installation](#installation)
  * [Local Development](#local-development)
  * [Production (on the web with a domain name)](#production--on-the-web-with-a-domain-name-)
- [Using](#using)


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
6. After a few minutes, the program will be running. You can check that software is running with the command `docker logs webapp`. When the system is ready to use, the response should end in a log in the terminal window like this: `✔ Compiled successfully.`



## Production (on the web with a domain name and password protection)



# Using



