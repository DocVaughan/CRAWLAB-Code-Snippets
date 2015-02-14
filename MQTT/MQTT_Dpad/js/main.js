// SocketIO functions when the document is ready
$(document).ready(function(){
    // Read and send the Dpad button states over a websocket
    var dpad = 0000;
    var timeout_up = $('#up');
    var timeout_down = $('#down');
    var timeout_right = $('#right');
    var timeout_left = $('#left');   
    
    $('#up').mousedown(function () {
        dpad = 1000;
//         timeout_up = setInterval(function () { 
//         }, 100);

        return false;
    });
    $('#up').mouseup(function () {
        dpad = 0000;
//         clearInterval(timeout_up);
        return false;

    });
    $('#up').mouseout(function () {
        dpad = 0000;
//         clearInterval(timeout_up);
        return false;

    });
    
    // right Button    
    $('#right').mousedown(function () {
        dpad = 0100;
        timeout_right = setInterval(function () { 
        }, 100);

        return false;
    });
    $('#right').mouseup(function () {
        dpad = 0000;
        clearInterval(timeout_right);
        return false;
    });
    $('#right').mouseout(function () {
        dpad = 0000;
        clearInterval(timeout_right);
        return false;
    });
    
    
    // Down Button    
    $('#down').mousedown(function () {
        dpad = 0010;
        timeout_down = setInterval(function () { 
        }, 100);

        return false;
    });
    $('#down').mouseup(function () {
        dpad = 0000;
        clearInterval(timeout_down);
        return false;
    });
    $('#down').mouseout(function () {
        dpad = 0000;
        clearInterval(timeout_down);
        return false;
    });
    
    // Left Button    
    $('#left').mousedown(function () {
        dpad = 0001;
        timeout_left = setInterval(function () { 
        }, 100);

        return false;
    });
    $('#left').mouseup(function () {
        dpad = 0000;
        clearInterval(timeout_left);
        return false;
    });
    $('#left').mouseout(function () {
        dpad = 0000;
        clearInterval(timeout_left);
        return false;
    });

//     
//     // Send the data over a websocket 10 times per second (100ms)
//     (function send_data_at_interval() {
//         socket.emit('my broadcast event', {data: dpad});
//         setTimeout(send_data_at_interval, 100);
//         })();  
});

// Set up the MQTT client
var client = new Messaging.Client("broker.mqttdashboard.com", 8000, "myclientid_" + parseInt(Math.random() * 100, 10));

 //Connect Options
 var options = {
     timeout: 3,
     //Gets Called if the connection has sucessfully been established
     onSuccess: function () {
         alert("Connected");
     },
     //Gets Called if the connection could not be established
     onFailure: function (message) {
         alert("Connection failed: " + message.errorMessage);
     }
 }; 

 //Gets  called if the websocket/mqtt connection gets disconnected for any reason
 client.onConnectionLost = function (responseObject) {
     //Depending on your scenario you could implement a reconnect logic here
     alert("connection lost: " + responseObject.errorMessage);
 };

 //Gets called whenever you receive a message for your subscriptions
 client.onMessageArrived = function (message) {
     //Do something with the push message you received
     $('#messages').append('<span>Topic: ' + message.destinationName + '  | ' + message.payloadString + '</span><br/>');
 };

 //Creates a new Messaging.Message Object and sends it to the HiveMQ MQTT Broker
 var publish = function (payload, topic, qos) {
     //Send your message (also possible to serialize it as JSON or protobuf or just use a string, no limitations)
     var message = new Messaging.Message(payload);
     message.destinationName = topic;
     message.qos = qos;
     client.send(message);
 }

 

