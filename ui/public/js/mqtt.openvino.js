var mqttclient;
//const mqtt = require('mqtt');
//var mqttclientconnectedtries = 0;
var MQTTOpenvino = {
    connect: function (messagecallback) {
        mqttclient = mqtt.connect("ws://" + MQTT.SERVER +":" + MQTT.PORT) // you add a ws:// url here
        mqttclient.subscribe(MQTT.TOPIC_TIME_INFERENCE, {qos:2});
        mqttclient.subscribe(MQTT.TOPIC_PERSON, {qos:2});
        mqttclient.subscribe(MQTT.TOPIC_RESOLUTION), {qos:2};
        mqttclient.subscribe(MQTT.TOPIC_FPS, {qos:2}); 
        mqttclient.subscribe(MQTT.TOPIC_TIME_INFERENCE_M, {qos:2});
        mqttclient.subscribe(MQTT.TOPIC_FPS_M, {qos:2});
        mqttclient.subscribe(MQTT.TOPIC_RESOLUTION_M, {qos:2});
        mqttclient.subscribe(MQTT.TOPIC_MASK, {qos:2}); 
        mqttclient.subscribe(MQTT.TOPIC_NO_MASK, {qos:2}); 
        mqttclient.subscribe(MQTT.TOPIC_TIME_INFERENCE_D, {qos:2});
        mqttclient.subscribe(MQTT.TOPIC_FPS_D, {qos:2});
        mqttclient.subscribe(MQTT.TOPIC_RESOLUTION_D, {qos:2});
        mqttclient.subscribe(MQTT.TOPIC_TOTAL, {qos:2}); 
        mqttclient.subscribe(MQTT.TOPIC_SAFE, {qos:2}); 
        mqttclient.subscribe(MQTT.TOPIC_LOWRISK, {qos:2}); 
        mqttclient.subscribe(MQTT.TOPIC_HIGHRISK, {qos:2}); 
        //mqttclient.subscribe(MQTT.TOPIC_FPS_MASK);
        mqttclient.on("message", function (topic, payload) {
           messagecallback(topic,payload); 
           //let m = payload.toString();
           setTimeout(MQTTOpenvino.connect, 200);
        });
    }
}