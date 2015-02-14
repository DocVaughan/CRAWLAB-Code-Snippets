// SocketIO functions when the document is ready
$(document).ready(function(){
    // Read and send the Dpad button states over a websocket
    var dpad = 0000;
    var timeout_up = $('#up');
    var timeout_down = $('#down');
    var timeout_right = $('#right');
    var timeout_left = $('#left');      
    
    console.log('Hello')
    console.log(dpad)
    
    // Set up the MQTT client
    client = new Messaging.Client("broker.mqttdashboard.com", 8000, "myclientid_" + parseInt(Math.random() * 100, 10));

    //Connect Options
    options = {
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

    client.connect(options);

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
     publish = function (payload, topic, qos) {
         //Send your message (also possible to serialize it as JSON or protobuf or just use a string, no limitations)
         var message = new Messaging.Message(payload);
         message.destinationName = topic;
         message.qos = qos;
         client.send(message);
    }
    
    
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
    
    $('#up').on("touchstart", function () {
        dpad = 1000;
        return false;
    });
    
    $('#up').on("touchend", function () {
        dpad = 0000;
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
    
    $('#right').on("touchstart", function () {
        dpad = 0100;
        return false;
    });
    
    $('#right').on("touchend", function () {
        dpad = 0000;
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
    
    $('#down').on("touchstart", function () {
        dpad = 0010;
        return false;
    });
    
    $('#down').on("touchend", function () {
        dpad = 0000;
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
    
    $('#left').on("touchstart", function () {
        dpad = 0001;
        return false;
    });
    
    $('#left').on("touchend", function () {
        dpad = 0000;
        return false;
    });

//     
//     // Send the data over a websocket 10 times per second (100ms)
//     (function send_data_at_interval() {
//         socket.emit('my broadcast event', {data: dpad});
//         setTimeout(send_data_at_interval, 100);
//         })();  

// Send the data over a MQTT 10 times per second (100ms)
 start_sending = function () {
     console.log('sending')
    //Send your message (also possible to serialize it as JSON or protobuf or just use a string, no limitations)
     var message = new Messaging.Message(String(dpad));
     message.destinationName = 'CRAWLAB';
     message.qos = 2;
     client.send(message);
    setTimeout(start_sending, 50);
    };  

});




