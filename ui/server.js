//MODULES
var express = require('express');
config = require('./server/configure');
var app= express();
var http = require('http').Server(app);


//CONFIG
app.set('port', process.env.PORT || 8080);
app.set('views', __dirname + '/views');
app = config(app);

http.listen(app.get('port'), function(){
	console.log('Server up: http://192.168.50.35:' + app.get('port'));
});
