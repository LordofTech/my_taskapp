const http = require('http');

const port = process.env.PORT || 3000; // Use environment variable for port or default to 3000

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello from your Node.js server!');
});

server.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
