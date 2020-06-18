var path = require('path');
var routes = require('./routes');
var exphbs = require('express-handlebars'); //for templates
var express = require('express');
var bodyParser = require('body-parser'); //http request fields management
var cookieParser = require('cookie-parser'); //cookies send and received
var morgan = require('morgan'); //for logging
var methodOverride = require('method-override');//for REST API in older browsers
var errorHandler = require('errorhandler');

//we receive our app, config it and return it
module.exports = function(app){
	app.use(morgan('dev'));
	app.use(bodyParser.urlencoded({'extended': true}));
	app.use(bodyParser.json());
	app.use(methodOverride());
	app.use(cookieParser('some-scret-value-here'));
	routes(app); //moving the routes to routes folder

	//important to define static middleware after routes
	app.use('/public/', express.static(path.join(__dirname,'../public')));

	if('development' === app.get('env')) {
		app.use(errorHandler());
	}

	app.engine('handlebars', exphbs.create({
		defaultLayout: 'main',
		layoutsDir: app.get('views' + '/layouts'),
		partialsDir: [app.get('views') + '/partials'] //usamos [] para recordar que se puede hacer, e incluir varias carpetas
	}).engine);
	app.set('view engine', 'handlebars');

	return app;

};
