FROM node

#USER root

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

WORKDIR /usr/src/app

## Fetch code from git
RUN git init && git remote add -f origin git@github.com:Telefonica/vision_valley_demo.git && git config core.sparseCheckout true && echo "mqtt_broker/" >> .git/info/sparse-checkout && git pull --depth=1 origin master

WORKDIR ./mqtt_broker

RUN npm install


#Expose API ports to the outside
EXPOSE 1883
EXPOSE 3000

#Launch application
CMD node server.js

