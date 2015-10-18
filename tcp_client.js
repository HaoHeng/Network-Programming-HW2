var net = require('net');

var HOST = '127.0.0.1';
var PORT = 5566;

var client = new net.Socket();
client.connect(PORT, HOST, function() {

    console.log('CONNECTED TO: ' + HOST + ':' + PORT);
    

});


console.log("Welcome to Game 2048!") ;
console.log("enter 'help' to get more information") ;

var i = client.createInterface(process.stdin, process.stdout, null);
  i.question('Write your name: ', function(answer) {
    console.log('Nice to meet you> ' + answer);
    i.close();
    process.stdin.destroy();

  });
