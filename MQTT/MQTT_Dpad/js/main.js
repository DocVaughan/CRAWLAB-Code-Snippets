// SocketIO functions when the document is ready
$(document).ready(function(){

    // Functions for the draggable joystick - implemented in Joystick.js
    vec = Object.seal({
    x: 0,
    y: 0
    });

//     tester = $('#tester');
//     tester.draggable();

    JoyStick('#joystick1', 120, function(magnitude, theta, ximpulse, yimpulse) {
//         console.log(magnitude, theta, ximpulse, yimpulse);

        vec.x = ximpulse; // 10 * (ximpulse / 80);
        vec.y = yimpulse; // 10 * (yimpulse / 80);
        
        if (vec.x > 100) {
            vec.x = 100;
        } else if (vec.x < -100) {
            vec.x = -100;
        } 
        
        if (vec.y > 100) {
            vec.y = 100;
        } else if (vec.y < -100) {
            vec.y = -100;
        } 
    });


    // Read and send the Dpad button states over MQTT
    var timeout_up = $('#up');
    var timeout_down = $('#down');
    var timeout_right = $('#right');
    var timeout_left = $('#left'); 
    var sending = false     
    
    // Set up the MQTT client
    client = new Messaging.Client("broker.mqttdashboard.com", 8000, "myclientid_" + parseInt(Math.random() * 100, 10));

    //Connect Options
    options = {
         timeout: 3,
         //Gets Called if the connection has sucessfully been established
         onSuccess: function () {
//              alert("Connected");
            $('.connected').toggleClass('on');
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
        $('.connected').toggleClass('on');
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
    
    // Up Button
    $('#up').mousedown(function () {
        vec.x = 0;
        vec.y = 100;
        dpad = "0,100";
        return false;
    });
    
    $('#up').mouseup(function () {
        vec.x = 0;
        vec.y = 0;
        return false;
    });
    
    $('#up').mouseout(function () {
        vec.x = 0;
        vec.y = 0;
        return false;
    });
    
    $('#up').on("touchstart", function () {
        vec.x = 0;
        vec.y = 100;
        return false;
    });
    
    $('#up').on("touchend", function () {
        vec.x = 0;
        vec.y = 0;
        return false;
    });
    

    // right Button    
    $('#right').mousedown(function () {
        vec.x = 100;
        vec.y = 0;
        timeout_right = setInterval(function () { 
        }, 100);

        return false;
    });
    
    $('#right').mouseup(function () {
        vec.x = 0;
        vec.y = 0;
        clearInterval(timeout_right);
        return false;
    });
    
    $('#right').mouseout(function () {
        vec.x = 0;
        vec.y = 0;
        clearInterval(timeout_right);
        return false;
    });
    
    $('#right').on("touchstart", function () {
        vec.x = 100;
        vec.y = 0;
        return false;
    });
    
    $('#right').on("touchend", function () {
        vec.x = 0;
        vec.y = 0;
        return false;
    });
    
    
    // Down Button    
    $('#down').mousedown(function () {
        vec.x = 0;
        vec.y = -100;
        return false;
    });
    
    $('#down').mouseup(function () {
        vec.x = 0;
        vec.y = 0;
        return false;
    });
    
    $('#down').mouseout(function () {
        vec.x = 0;
        vec.y = 0;
        return false;
    });
    
    $('#down').on("touchstart", function () {
        vec.x = 0;
        vec.y = -100;
        return false;
    });
    
    $('#down').on("touchend", function () {
        vec.x = 0;
        vec.y = 0;
        return false;
    });
    
    
    // Left Button    
    $('#left').mousedown(function () {
        vec.x = -100;
        vec.y = 0;
        timeout_left = setInterval(function () { 
        }, 100);
        return false;
    });
    
    $('#left').mouseup(function () {
        vec.x = 0;
        vec.y = 0;
        clearInterval(timeout_left);
        return false;
    });
    
    $('#left').mouseout(function () {
        vec.x = 0;
        vec.y = 0;
        clearInterval(timeout_left);
        return false;
    });
    
    $('#left').on("touchstart", function () {
        vec.x = -100;
        vec.y = 0;
        return false;
    });
    
    $('#left').on("touchend", function () {
        vec.x = 0;
        vec.y = 0;
        return false;
    });


// Send the data over a MQTT 10 times per second (100ms)
toggle_sending = function () {
    if (sending) {
        if (timer) {
         clearTimeout(timer);
         timer = 0;
         $('#control').text('Start');
         sending = false;
        $('.sending').toggleClass('on');
        }
    }
    else {
        $("#control").text('Stop');
        $(".send_status").css("background-color","red");
        sending = true;
        //Send your message (also possible to serialize it as JSON or protobuf or just use a string, no limitations)
        send_data();
        $('.sending').toggleClass('on');
        };  
    }
send_data = function (){
//Send your message (also possible to serialize it as JSON or protobuf or just use a string, no limitations)
         var message = new Messaging.Message(String(vec.x) + ',' + String(vec.y));
         message.destinationName = 'CRAWLAB';
         message.qos = 0;
         client.send(message);
        timer = setTimeout(send_data, 50);
        }
});




