var http = require('http');

http.createServer(function (request, response) {
    response.writeHead(200, {'Content-type': 'text/plain'});
    response.end('Hello World\n');
}).listen(8124);

console.log('Server running at http://127.0.0.1:8124/');
console.log(__filename);
console.log(__dirname);
console.log('count: %d', 100);
console.time('xx')
