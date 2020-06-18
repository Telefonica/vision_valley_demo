FROM node


RUN rm /bin/sh && ln -s /bin/bash /bin/sh

WORKDIR /usr/src/app

# add credentials on build
ARG SSH_PRIVATE_KEY
ARG SSH_PUBLIC_KEY
RUN mkdir /root/.ssh/
RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa && \
    echo "${SSH_PUBLIC_KEY}" > /root/.ssh/id_rsa.pub && \
    chmod 600 /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa.pub && \
    ssh-keyscan github.com >> /root/.ssh/known_hosts && \
    eval `ssh-agent -s` && \
    ssh-add

## Fetch code from git
RUN git init && git remote add -f origin git@github.com:d-rom/cvdemo-5ghacking.git && git config core.sparseCheckout true && echo "ui/" >> .git/info/sparse-checkout && git pull --depth=1 origin master

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

