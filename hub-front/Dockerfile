# base image
FROM node:12.2.0

# install chrome for protractor tests
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update && apt-get install -yq google-chrome-stable

# set working directory
WORKDIR /app


# add `/app/node_modules/.bin` to $PATH

# add app
COPY . /app

ENV PATH /app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /app/package.json
RUN npm install
RUN npm install -g @angular/cli@11.2.5
RUN npm link @angular/cli



# start app
CMD ng serve --host 0.0.0.0

# WORKDIR /app/dist/webapp/

# COPY nodeserver.js /app/dist/webapp/nodeserver.js

# EXPOSE 9001

# CMD ["tail", "-f", "/dev/null"]


#CMD [ "node", "nodeserver.js" ]