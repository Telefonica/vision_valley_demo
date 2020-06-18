var express = require('express'),
	router = express.Router(),
	home = require('../controllers/home');
	people = require('../controllers/people');
	mask = require('../controllers/mask');
	distance = require('../controllers/distance');

module.exports = function(app){
	router.get('/', home.index);
	router.get('/crowdEventDetection', people.index);
	router.get('/faceMaskMonitor', mask.index);
	router.get('/socialDistanceMonitor', distance.index);
	app.use(router);
};