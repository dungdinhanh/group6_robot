// const serverUrl = '130.238.93.215'
const serverUrl = 'localhost'
ws = new WebSocket("ws://" + serverUrl + ":8888");
var canvas = document.getElementById('canvas-video');
var context = canvas.getContext('2d');
var map = document.getElementById('canvas-map');
var mapContext = map.getContext('2d');

var currentDpDisplay = document.getElementById('current-dp');
var destinationDpDisplay = document.getElementById('destination-dp');
var humidityDisplay = document.getElementById('humidity');
var temperatureDisplay = document.getElementById('temperature');
var commandsDisplay = document.getElementById('commands');
var waitingOnRobot = document.getElementById('waiting-on-robot');

var dropoffPoints = [
  {
    id: 0,
    x: 100,
    y: 10,
    name: "Point 1"
  },
  {
    id: 1,
    x: 300,
    y: 10,
    name: "Point 2"
  },
  {
    id: 2,
    x: 500,
    y: 10,
    name: "Point 3"
  },
  {
    id: 3,
    x: 10,
    y: 300,
    name: "Point 4"
  },
  {
    id: 4,
    x: 590,
    y: 300,
    name: "Point 5"
  },
  {
    id: 5,
    type: "INTERSECTION",
    x: 100,
    y: 300,
    name: "Intersection 1"
  },
  {
    id: 6,
    type: "INTERSECTION",
    x: 300,
    y: 300,
    name: "Intersection 2"
  },
  {
    id: 7,
    type: "INTERSECTION",
    x: 500,
    y: 300,
    name: "Intersection 3"
  },
  {
    id: 8,
    type: "INITIAL",
    x: 300,
    y: 590,
    name: "Start position"
  }
];


const dropoffPointSize = { width: 10, height: 0 };
const dropoffTouchRecognitionSize = { width: 40, height: 40 };


/*1: forward
2: backward
3: left
4: right
5: down
6: up*/

function stringFromCommand(cmd) {
  switch (cmd) {
    case 1: return "forward";
    case 2: return "backward";
    case 3: return "left";
    case 4: return "right";
    case 5: return "down";
    case 6: return "up";
    default: return ""
  }
}
function stringFromCommands(cmds) {
  return cmds.map(cmd => stringFromCommand(cmd))
}

function drawPoints(dropoffPoints) {
  mapContext.fillStyle = "red";
  for (var i = 0; i < dropoffPoints.length; i++) {
    const dp = dropoffPoints[i];
    mapContext.fillStyle = dp.type === "INITIAL"
      ? "blue"
      : (dp.type === "INTERSECTION"
        ? "yellow"
        : "red")
    mapContext.beginPath();
    mapContext.arc(dp.x, dp.y, dropoffPointSize.width, dropoffPointSize.height, 2 * Math.PI);
    mapContext.fill();
  }
}

function drawGrid() {
  mapContext.strokeStyle = "#000000"
  mapContext.lineWidth = 10;
  mapContext.beginPath();
  mapContext.moveTo(100, 0);
  mapContext.lineTo(100, 300);
  mapContext.stroke();
  mapContext.beginPath();
  mapContext.moveTo(300, 0);
  mapContext.lineTo(300, 600);
  mapContext.stroke();
  mapContext.beginPath();
  mapContext.moveTo(500, 0);
  mapContext.lineTo(500, 300);
  mapContext.stroke();
  mapContext.beginPath();
  mapContext.moveTo(0, 300);
  mapContext.lineTo(600, 300);
  mapContext.stroke();
}

const robotSize = { width: 30, height: 30 }

function updateMap(dropOffId) {
  console.log("Move robot commands");
  const dp = dropoffPoints.find(d => d.id === dropOffId);
  if (dp) {
    mapContext.clearRect(0, 0, 600, 600);
    drawGrid()
    drawPoints(dropoffPoints)
    mapContext.fillStyle = "blue";
    mapContext.fillRect(dp.x - robotSize.width / 2, dp.y - robotSize.height / 2, robotSize.width, robotSize.height);
  }
}

function isInside(pos, rect) {
  return pos.x > rect.x - (rect.width / 2) && pos.x < rect.x + (rect.width / 2) && pos.y < rect.y + (rect.height / 2) && pos.y > rect.y - (rect.height / 2)
}

function isInsideDropoffPoint(pos) {
  for (var i = 0; i < dropoffPoints.length; i++) {
    const point = dropoffPoints[i];
    if (point !== "INITIAL") {
      const rect = {
        x: point.x,
        y: point.y,
        width: dropoffTouchRecognitionSize.width,
        height: dropoffTouchRecognitionSize.height
      };
      console.log("Rect", rect);
      console.log("Mouse position", pos);
      if (isInside(pos, rect)) {
        return point;
      }
    }
  }
  return null;
}

function getMousePos(canvas, event) {
  var rect = canvas.getBoundingClientRect();
  console.log("Rect", rect);
  return {
    x: event.clientX - rect.left,
    y: event.clientY - rect.top
  };
}

map.addEventListener('click', function (evt) {
  var mousePos = getMousePos(map, evt);
  var selectedDp = isInsideDropoffPoint(mousePos);
  if (selectedDp) {
    fetch('http://' + serverUrl + ':4000/commands', {
      body: JSON.stringify({
        destinationPoint: selectedDp.id
      }),
      headers: {
        'content-type': 'application/json'
      },
      method: 'POST'
    })
      .then(response => response.json())
      .then(json => {
        json.unshift(6);
        json.push(5);
        console.log(json)
        fetch('http://localhost:8080', {
          body: JSON.stringify({
            list_action: json,
            default: 'on'
          }),
          // headers: {
          //   'content-type': 'application/json'
          // },
          method: 'POST'
        })
          .then(response => response.json())
          .then(json => console.log('Data from robot server after send list_actions', json))
      })
  }
}, false);

function updateDisplay(destDp, currentDp, humidity, temperature, commands) {
  destinationDpDisplay.innerHTML = dropoffPoints[destDp] ? dropoffPoints[destDp].name : "";
  currentDpDisplay.innerHTML = dropoffPoints[currentDp] ? dropoffPoints[currentDp].name : "";
  humidityDisplay.innerHTML = humidity ? humidity : "";
  temperatureDisplay.innerHTML = temperature ? temperature : "";
  commandsDisplay.innerHTML = commands ? stringFromCommands(commands) : "";
  waitingOnRobot.innerHTML = destDp ? "Waiting on robot" : ""
}

function onRobotMessage(message) {
  updateMap(message.currentPoint);
  updateDisplay(message.destinationPoint, message.currentPoint, message.humidity, message.temperature, message.commands);
}

ws.onmessage = function (json) {
  var message = JSON.parse(json.data);
  switch (message.type) {
    case 'frame':
      var img = new Image();
      img.onload = function () {
        context.drawImage(img, 0, 0);
      };
      img.src = "data:image/jpg;base64," + message.data;
      break;
    case 'robot':
      console.log("Robot", message);
      onRobotMessage(JSON.parse(message.data));
      break;
    default: break;
  }
}