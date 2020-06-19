FROM tiangolo/nginx-rtmp

WORKDIR ./

USER root


## Fetch code from git
RUN git init && git remote add -f origin git@github.com:Telefonica/vision_valley_demo.git && git config core.sparseCheckout true && echo "streaming_server/" >> .git/info/sparse-checkout && git pull --depth=1 origin master

WORKDIR ./streaming_server

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 8090