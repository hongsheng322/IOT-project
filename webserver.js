var http = require('http').createServer(handler); //require http server, and create server with function handler()
var fs = require('fs'); //require filesystem module
const io = require('socket.io')(http, {
    cors: {
        origin: "http://localhost:8080",
        methods: ["GET", "POST"],
        transports: ['websocket', 'polling'],
        credentials: true
    },
    allowEIO3: true
});
var Gpio = require('onoff').Gpio; //include onoff to interact with the GPIO
var flameSensor = new Gpio(21, 'in', 'both', {debounceTimeout: 100}); //use GPIO pin 21 as output

http.listen(8080); //listen to port 8080

function handler (req, res) { //create server
    fs.readFile(__dirname + '/public/index.html', function(err, data) { //read file index.html in public folder
      if (err) {
        res.writeHead(404, {'Content-Type': 'text/html'}); //display 404 on error
        return res.end("404 Not Found");
      }
      res.writeHead(200, {'Content-Type': 'text/html'}); //write HTML
      res.write(data); //write data from index.html
      return res.end();
      });
}
 
//test
io.sockets.on('connection', function (socket) {// WebSocket Connection
    // checks for flame every 200ms
    const flameDetection = _ => {  
      var flamevalue = 0; //static variable for current status
      flameSensor.read((err, value) => { // Asynchronous read
        if (err) {
          throw err;
        }
        flamevalue = boolflip(value); // not sure why the detection values are opposite so i flipped them
        console.log(flamevalue);
        socket.emit('light', flamevalue);
      });

    setTimeout(flameDetection, 200);
};
    flameDetection();
});

function boolflip(value){
    if(value == 1)
        return 0
    else
        return 1
}




process.on('SIGINT', function () { //on ctrl+c
  flameSensor.unexport(); // Unexport LED GPIO to free resources
  process.exit(); //exit completely
});