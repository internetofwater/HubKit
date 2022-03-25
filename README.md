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
4. Modify the `docker-compose.yml` file, changing "yourdomain.com" to the desired subdomain you registered in the code block below. Depending his can be done with command line tools like [vi]() or [nano]().
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
10. `git clone https://github.com/{your github name}/HubKit
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

  Change `hubkit` to what you would like the username to be. Change `JDJhJDE0JFA5bXRCQ1VCTVM1bUF6bzJRVTdKaC5BalE4V2pUL1RxZEJtTlREOXRROFlCNE9uNEI2YTVx` to the hash of your desired password. To create a password hash, 

# Using



