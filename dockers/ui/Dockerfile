FROM node


RUN rm /bin/sh && ln -s /bin/bash /bin/sh

WORKDIR /usr/src/app

## Fetch code from git
RUN git init && git remote add -f origin git@github.com:Telefonica/vision_valley_demo.git && git config core.sparseCheckout true && echo "ui/" >> .git/info/sparse-checkout && git pull --depth=1 origin master

WORKDIR ./ui

#COPY package*.json ./

RUN npm install


#Expose API ports to the outside
EXPOSE 8080
EXPOSE 3000
EXPOSE 8090

#Launch application
COPY . .
CMD node server.js

