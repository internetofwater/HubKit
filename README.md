# HubKit
Making a HubKit based on SensorThings API and PyGeoAPI


# Run Docker via 
Start the docker container do this. 
cd hub-front && docker build -t webapp:dev . && cd ../
cd hub-back && docker build -t python:dev . && cd ../
cd devops && docker-compose up && cd../

# When you're all done.
docker rm webapp api


# Run Docker Via Command Line
docker run -v ${PWD}:/app -v /app/node_modules -p 4200:4200 --name webapp --rm webapp:dev

cd ../hub-back && docker build -t python:dev . 
docker run -v ${PWD}:/app -p 5000:5000 --name api --rm python:dev 


# Run tests
docker exec -it foo ng test --watch=false
docker exec -it foo ng e2e --port 4202



