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

# Installation

The easiest way to install HubKit is to use our Docker images and `docker-compose`. In this way, the only prerequisite is a server with Docker and docker-compose installed. 

* [Instructions to install Docker and docker-compose on Mac or Windows Desktop environments](https://docs.docker.com/get-docker/)
* Instructions to install Docker on a Linux server: [(see "Installation per Distro" for instructions depending on which Linux version)](https://docs.docker.com/engine/install/)
* [Instructions to install docker-compose](https://docs.docker.com/compose/install/)

You can copy all of the source code for the repository for local development in a local directory. Clone this repository, i.e.

`git clone https://github.com/internetofwater/HubKit.git`

You may have to [install git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), if it is not installed on your machine

## Local Testing

1. Make a local directory (folder) on your computer, e.g. `mkdir HubKit`
2. In a Terminal on a Mac or Linux machine, or a Powershell on a Windows machine, navigate to that directory, e.g. ```cd ~/HubKit```
3. In this folder, clone this repository



## Production (on the web with a domain name)



# Using



