var config;
var server;
const aedes = require('aedes')();
const httpServer = require('http').createServer();
const ws = require('websocket-stream');

module.exports = {
    configure: function (c) {
        config = c;
    },

    start: function () {
        server = new require('net').createServer(aedes.handle);
        ws.createServer({ server: httpServer }, aedes.handle);

        var port = config.mqtt.port;
        var http_port = config.mqtt.http.port;

        server.listen(port, function() {
            console.log('Aedes MQTT listening on port: ' + port)
        });   

        httpServer.listen(http_port, function () {
            console.log('Aedes MQTT-WS listening on port: ' + http_port);
        })    

        server.on('clientReady', setup);
        server.on('clientConnected', connected);
        server.on('clientError', unaccessible);
        server.on('clientDisconnect', disconnected);
        server.on('publish', published);
        server.on('subscribe', subscribed);
        server.on('unsubscribe', unsubscribed);
    },

    publish: function (topic, message) {
        var payload = {
            cmd: 'publish',
            topic: topic,
            payload: message,
            qos: 1,
            retain: false
        };
        aedes.publish(payload);
        /*var http_port = config.mqtt.http.port;
        httpServer.listen(http_port, function () {
            console.log('Aedes MQTT-WS listening on port: ' + http_port);
            aedes.publish(payload);
        });*/
    }
};

function setup() {
    console.log('Aedes server started.');
}

function connected(client) {
    console.log(`Client ${client.id} connected`);
}

function unaccessible(client) {
    console.log(`Client ${client.id} counld NOT connect`);
}

function subscribed(topic, client) {
    console.log(`Client ${client.id} subscribed to ${topic}.`);
}

function unsubscribed(topic, client) {
    console.log(`Client ${client.id} unsubscribed from ${topic}.`);
}

function disconnected(client) {
    console.log(`Client ${client.id}`);
}

function published(packet, client) {
    //console.log(`Published to ${packet.topic} <- ${packet.payload}`);
}
