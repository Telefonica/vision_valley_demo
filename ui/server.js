//MODULES
var express = require('express');
config = require('./server/configure');
var app= express();
var http = require('http').Server(app);


//CONFIG
app.set('port', process.env.PORT || 8080);
app.set('views', __dirname + '/views');
app = config(app);

app.locals.config = require('./public/js/conf')

http.listen(app.get('port'), function(){
	//console.log('Server up: http://' + app.locals.CONF.RENDERING_IP + ':' + app.get('port'));
	console.log('Server up: http://localhost:' + app.get('port'));
});
