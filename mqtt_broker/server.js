var mqtt = require('./mqtt');
const config = require('./config');

mqtt.configure(config);
mqtt.start();//iniciamos el servidor mqtt

