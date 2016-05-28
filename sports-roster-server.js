var express = require('express');
var fs = require("fs");
var app = express();

function readJsonFile(file){
	var filepath = __dirname + '/' + file;
	var file = fs.readFileSync(filepath, 'utf8');
	return JSON.parse(file);
}

var jsonFiles = {
	'nfl': readJsonFile('./nfl.json'),
	'nba': readJsonFile('./nba.json'),
	'ncaa_football': readJsonFile('./ncaa_football.json'),
	'ncaa_basketball': readJsonFile('./ncaa_basketball.json'),
}

app.get('/api/:league', function (request, response) {
	console.log(request.method + ": " + request.url);
	response.json(jsonFiles[request.params.league]);
});

app.get('/api/:league/:teamid', function (request, response) {
	console.log(request.method + ": " + request.url);
	response.json(jsonFiles[request.params.league][request.params.teamid]);
});

app.get('/api/:league/:teamid/:playernumber', function (request, response) {
	console.log(request.method + ": " + request.url);
	var playersWithNumber = [];
	for (key in jsonFiles[request.params.league][request.params.teamid]['roster']) {
		var player = jsonFiles[request.params.league][request.params.teamid]['roster'][key];
		if (player['NO'] === request.params.playernumber ||
			player['NO.'] === request.params.playernumber) {
			playersWithNumber.push(player);
		}
	}
	response.json(playersWithNumber);
});

var server_port = process.env.OPENSHIFT_NODEJS_PORT || 8080;
var server_ip_address = process.env.OPENSHIFT_NODEJS_IP || '127.0.0.1';
var server = app.listen(server_port, server_ip_address, function () {
	console.log("Listening on " + server_ip_address + ", server_port " + server_port);
});