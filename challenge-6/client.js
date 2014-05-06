#!/usr/bin/env node

if ((process.version.split('.')[1]|0) < 10) {
	console.log('Please, upgrade your node version to 0.10+');
	process.exit();
}

var net = require('net');
var util = require('util');
var crypto = require('crypto');

var options = {
	'port': 6969,
	'host': '54.83.207.90',
}

var KEYPHRASE;

process.stdin.resume();
process.stdin.setEncoding('utf8');
process.stdin.on('data', function (data) {
  KEYPHRASE = data.trim();
});

var state = 0;
var my_dh, my_prime, my_public_key, my_secret;

var socket = net.connect(options, function() {
  state++;
});


socket.on('data', function(data) {

	direction = data.toString().trim().split(':')[0];
  true_data = data.toString().trim().split(':')[1].split('|');

  if (state == 1 && true_data[0] == 'hello?') {
    socket.write("hello?");
    state++;
  } else if (state == 2 && true_data[0] == 'hello!') {
    socket.write("hello!");
    state++;
  } else if (state == 3 && true_data[0] == 'key') {
    my_dh = crypto.createDiffieHellman(256);
    my_dh.generateKeys();
    my_prime = my_dh.getPrime('hex');
    my_public_key = my_dh.getPublicKey('hex');
    // Pass my public key as the backdoor computer public key
    socket.write(util.format('key|%s|%s\n', my_prime, my_public_key));
    state++;
  } else if (state == 4 && true_data[0] == 'key') {
    // Retrieve public key from server
    server_public_key = true_data[1];
    socket.write(util.format('key|%s\n', server_public_key));
    state++;
  } else if (state == 5 && true_data[0] == 'keyphrase') {
    my_secret = my_dh.computeSecret(server_public_key, 'hex');
    var cipher = crypto.createCipheriv('aes-256-ecb', my_secret, '');
    // Encode keyphrase
    var keyphrase = cipher.update(KEYPHRASE, 'utf8', 'hex') + cipher.final('hex');
    socket.write(util.format('keyphrase|%s\n', keyphrase));
    state++;
  } else if (state == 6 && true_data[0] == 'result') {
    var decipher = crypto.createDecipheriv('aes-256-ecb', my_secret , '');
    // Decode message
    var keyphrase = decipher.update(true_data[1], 'hex', 'utf8') + decipher.final('utf8');
    console.log(keyphrase);
    socket.end();
  } else {
    console.log('Error');
    socket.end();
  }
});
