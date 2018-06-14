const path = require('path')
const paths = require("./paths");
const bodyParser = require("body-parser");
const WebSocket = require("ws");
const express = require("express");
const cors = require("cors");
const app = express();
const fps = 60;
const camInterval = 1000 / fps;

const wss = new WebSocket.Server({
  port: 8888
});

let isWaiting = false;

const sendMessage = (client, type, data) => {
  const message = { type, data };
  const jsonMessage = JSON.stringify(message);
  client.send(jsonMessage);
};

const broadcast = (type, data) => {
  wss.clients.forEach(function each(client) {
    if (client.readyState === WebSocket.OPEN) {
      sendMessage(client, type, data);
    }
  });
};

function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

let _humidity = "good";
let _temperature = "acceptable";
let _currentPoint = 8;
let _destinationPoint = null;
let _commands = [];

app.use(cors());
app.use(bodyParser.text());
app.use(bodyParser.json());

const mockRobotResponse = () => {
  const conditions = ["good", "acceptable", "bad"];
  _humidity = conditions[getRandomInt(2)];
  _temperature = conditions[getRandomInt(2)];
  _currentPoint = _destinationPoint;
  _destinationPoint = null;
};
const sendDataToClient = () => {
  broadcast(
    "robot",
    JSON.stringify({
      humidity: _humidity,
      temperature: _temperature,
      destinationPoint: _destinationPoint,
      currentPoint: _currentPoint,
      commands: _commands
    })
  );
};

app.get('*', (req, res) => {
  res.send('Please open index.html directly');
})

app.post("/commands", (req, res) => {
  console.log('Get to post /commands')
  if (isWaiting) {
    res.send('Waiting for robot response')
  }
  else if (_destinationPoint === null) {
    console.log("Req", req.body);
    const { destinationPoint } = req.body;
    _commands = paths.paths[_currentPoint][destinationPoint];
    res.send(JSON.stringify(_commands));
    _destinationPoint = destinationPoint;
    sendDataToClient();
  }
});

app.post("/response", (req, res) => {
  console.log(req.body)
  const robotData = JSON.parse(req.body)
  _humidity = 1;
  _temperature = 1;
  _currentPoint = robotData.currentPoint;
  _destinationPoint = null;
  sendDataToClient();
})

app.listen(4000, () => {
  console.log("Control server up");
});

wss.on("connection", function (ws) {
  console.log("Connection");
  sendMessage(
    ws,
    "robot",
    JSON.stringify({
      humidity: _humidity,
      temperature: _temperature,
      destinationPoint: _destinationPoint,
      currentPoint: _currentPoint,
      commands: _commands
    })
  );
  // try {
  //   var camera = new cv.VideoCapture(0);
  //   setInterval(() => {
  //     camera.read((err, data) => {
  //       if (err) throw err;
  //       const raw = data.toBuffer().toString("base64");

  //       broadcast("frame", raw);
  //     });
  //   }, camInterval);
  // } catch (e) {
  //   console.log("Couldn't start camera:", e);
  // }
});
