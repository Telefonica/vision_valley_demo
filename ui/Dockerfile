FROM node

#USER root

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

WORKDIR /usr/src/app

COPY .vision-valley-demo/ui/package*.json ./

RUN npm install


#Expose API ports to the outside
EXPOSE 8080
EXPOSE 3000
EXPOSE 8090

#Launch application
COPY . .
CMD node server.js

