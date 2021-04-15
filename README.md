# HubKit
Making a HubKit based on SensorThings API and PyGeoAPI



Start the docker container do this. 

cd hub-front && docker build -t webapp:dev . && cd ../
cd hub-back && docker build -t python:dev . && cd ../
cd devops && docker-compose up



docker run -d -v ${PWD}:/app -v /app/node_modules -p 4200:4200 --name webapp --rm webapp:dev

cd ../hub-back && docker build -t python:dev . 
docker run -d -v ${PWD}:/app -p 5000:5000 --name api --rm python:dev 



