const https = require('https');
const fs = require('fs');
const next = require('next');

const app = next({ dev: true });
const handle = app.getRequestHandler();

const options = {
  key: fs.readFileSync('cert/localhost-key.pem'),
  cert: fs.readFileSync('cert/localhost.pem'),
};

app.prepare().then(() => {
  https.createServer(options, (req, res) => handle(req, res)).listen(443, () => {
    console.log('Frontend running on https://localhost');
  });
});