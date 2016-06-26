// SocketIO functions when the document is ready
$(document).ready(function(){
    // Functions for the draggable joystick - implemented in Joystick.js
    vec = Object.seal({
    x: 0,
    y: 0
    });
    
    // Time variables
    var date = new Date();
    var start_Time = date.getTime();
    var time_elapsed = date.getTime() - start_Time;
    
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

    var x_received = 0;
    var y_received = 0;
    var dps_x = [];         // dataPoints
    var dps_y = [];         // dataPoints
    var dataLength = 100;   // number of dataPoints visible at any point
    var received_string;    // string to hold data received for parsing

    var chart = new CanvasJS.Chart("chartContainer",{	
        data: [
        {
            type: "line",
            markerType: "none",
            dataPoints: dps_x
        },
        {
            type: "line",
            markerType: "none",
            dataPoints: dps_y
        }],
        axisX:{
            title: "Time (s)",
            interval: 0.5,
         },
        axisY:{
            minimum: -110,
            maximum: 110,
         },
    });

    var updateChart = function () {
        dps_x.push({
            x: time_elapsed,
            y: x_received
        });
        
        dps_y.push({
            x: time_elapsed,
            y: y_received
        });
        
        if (dps_x.length > dataLength || dps_y.length > dataLength)
        {
            dps_x.shift();
            dps_y.shift();
        }
        
        chart.render();
    };

    // generates first set of dataPoints
    updateChart(dataLength); 

    // Read and send the Dpad button states over MQTT
    var timeout_up = $('#up');
    var timeout_down = $('#down');
    var timeout_right = $('#right');
    var timeout_left = $('#left'); 
    var sending = false;  
    var receiving = false;   
    var subscribed = false;
    var connected = false;

    // Set up the MQTT client    
    // iot.eclipse.org is default
    server = "iot.eclipse.org"
    port = 80
    client = new Messaging.Client(server, port, "CRAWLAB_" + parseInt(Math.random() * 100, 10));

    
    // Select the MQTT server to use
    $("#server" ).on('change', function() {
        $('.receiving').toggleClass('on', false);
        if (connected) {
            client.disconnect();
            sending = false;  
            receiving = false;   
            subscribed = false;
            $('.connected').toggleClass('on', false);
            $('.sending').toggleClass('on', false);
            $('.subscribed').toggleClass('on', false);
            $('.receiving').toggleClass('on', false);
            $('#receive').text('Receive');
            $('#control').text('Start');
            
        }
        server = $(this).val();
        select = document.getElementById('#server');
        console.log(server);
        
        if (server == "iot.eclipse.org") {
            port = 80;
        }
        else if (server == "test.mosquitto.org") {
            port = 8080;
        }
        else if (server == "broker.mqtt-dashboard.com") {
            port = 8000;
        }
        client = new Messaging.Client(server, port, "CRAWLAB_" + parseInt(Math.random() * 100, 10));
        client.connect(options)
        
        //Gets  called if the websocket/mqtt connection gets disconnected for any reason
        client.onConnectionLost = function (responseObject) {
        //Depending on your scenario you could implement a reconnect logic here
        //alert("Connection Lost: " + responseObject.errorMessage);
        $('.connected').toggleClass('on');
        connected = false;
        };

        //Gets called whenever you receive a message for your subscriptions
        client.onMessageArrived = function (message) {
        //Do something with the push message you received
        if (receiving) {
            $('#messages').prepend('<span>Topic: ' + message.destinationName + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data: ' + message.payloadString + '</span><br/>');
        }
        };
    });
    
    //Connect Options
    options = {
         timeout: 3,
         //Gets Called if the connection has sucessfully been established
         onSuccess: function () {
//              alert("Connected");
            $('.connected').toggleClass('on');
            connected = true;
         },
         //Gets Called if the connection could not be established
         onFailure: function (message) {
             alert("Connection failed: " + message.errorMessage);
             $('.connected').toggleClass('on', false);
             connected = false;
         }
     }; 

    client.connect(options);

            //Gets  called if the websocket/mqtt connection gets disconnected for any reason
    client.onConnectionLost = function (responseObject) {
        //Depending on your scenario you could implement a reconnect logic here
        //alert("Connection Lost: " + responseObject.errorMessage);
        $('.connected').toggleClass('on');
        connected = false;
    };

    //Gets called whenever you receive a message for your subscriptions
    client.onMessageArrived = function (message) {
        //Do something with the push message you received
        if (receiving) {
        $('#messages').prepend('<span>Topic: ' + message.destinationName + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data: ' + message.payloadString + '</span><br/>');
        received_string = message.payloadString.split(",");
        x_received = parseInt(received_string[0]);
        y_received = parseInt(received_string[1]);
        time_elapsed = (new Date() - start_Time) / 1000;
        console.log(time_elapsed);
        updateChart();
        }
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
         message.destinationName = 'CRAWLAB/test';
         message.qos = 0;
         client.send(message);
        timer = setTimeout(send_data, 50);
        }
        
// Accept the data being sent
toggle_receiving = function () {
    if (receiving) {
         $('#receive').text('Receive');
         receiving = false;
        $('.receiving').toggleClass('on');
    }
    else 
    {
        if (subscribed) {
            $("#receive").text('Stop');
            receiving = true;
            $('.receiving').toggleClass('on');
            $('#messages').text('');
            }
        else {
            alert("You must be subscribed to a topic to receive data published to it. Please subscribe and try again.")
        }
        
    }
    };
    
// Toggle susbscription
toggle_subscription = function () {
    if (subscribed) {
        $('.subscribed').toggleClass('on');
        client.unsubscribe('CRAWLAB/test');
        subscribed = false;
    }
    else {
        $('.subscribed').toggleClass('on');
        client.subscribe('CRAWLAB/test', {qos: 0});
        subscribed = true;
    }
    };
     
});

$(function navigation() {
	   // To make dropdown actually work
	   // To make more unobtrusive: http://css-tricks.com/4064-unobtrusive-page-changer/
      $("nav select").change(function() {
        window.location = $(this).find("option:selected").val();
      });
	 
	 });



