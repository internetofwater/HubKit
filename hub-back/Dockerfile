# base image
FROM ubuntu:20.04

# # install chrome for protractor tests
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get -qq -y install curl


RUN apt-get install python3 -y
RUN apt-get install python3-pip -y

RUN apt-get install virtualenv -y
RUN apt-get install vim -y


# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements /app/requirements

WORKDIR /app
COPY . /app

RUN rm -rf venv
# RUN virtualenv -p python3 venv
RUN pip3 install -r requirements/development.txt 

# DB STUFF
RUN apt-get install systemctl



# CMD ["tail", "-f", "/dev/null"]

ENTRYPOINT [ "python3" ]

CMD [ "runserver.py", "--environment=development", "--host=0.0.0.0" ]

# CMD ["tail", "-f", "/dev/null"]



# RUN npm install
# RUN npm install -g @angular/cli@7.3.9

# # add app
# COPY . /app

# # start app
# CMD ng serve --host 0.0.0.0

# WORKDIR /app/dist/webapp/

# COPY nodeserver.js /app/dist/webapp/nodeserver.js

# EXPOSE 9001

# CMD ["tail", "-f", "/dev/null"]


