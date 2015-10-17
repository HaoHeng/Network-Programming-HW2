var net = require('net');

var HOST = '127.0.0.1';
var PORT = 5566;

var client = new net.Socket();
client.connect(PORT, HOST, function() {

    console.log('CONNECTED TO: ' + HOST + ':' + PORT);
    

});