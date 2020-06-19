FROM node

#USER root

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

WORKDIR /usr/src/app
COPY ./mqtt_broker/package*.json ./

RUN npm install


#Expose API ports to the outside
EXPOSE 1883
EXPOSE 3000

#Launch application
COPY ./mqtt_broker/. .
CMD node server.js

