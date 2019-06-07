// SocketIO functions when the document is ready
$(document).ready(function(){
    // Functions for the draggable joystick - implemented in Joystick.js
    vec = Object.seal({
    x: 0,
    y: 0
    });

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

    // Set the scaling of the velocities in the twist message. It expects m/s
    // and our joystick parsing is set up for percentages of max
    var max_forward = 1.0  // m/s
    var max_ang_vel = 0.5  // rad/s

    // Read and send the Dpad button states over MQTT
    var timeout_up = $('#up');
    var timeout_down = $('#down');
    var timeout_right = $('#right');
    var timeout_left = $('#left'); 
    var sending = false;  
    var receiving = false;   
    var subscribed = false;
    var connected = false;

    // Connecting to ROS
    // -----------------
    var ros = new ROSLIB.Ros();

    // If there is an error on the backend, an 'error' emit will be emitted.
    ros.on('error', function(error) {
        console.log(error);
    });

    // Find out exactly when we made a connection.
    ros.on('connection', function() {
        console.log('Connection made!');
        connected = true;
        sending = false;  
        receiving = false;   
        subscribed = false;
        $('.connected').toggleClass('on', true);
        $('.sending').toggleClass('on', false);
        $('.subscribed').toggleClass('on', false);
        $('.receiving').toggleClass('on', false);
        $('#receive').text('Receive');
        $('#control').text('Start');
    });

    ros.on('close', function() {
        console.log('Connection closed.');
        $('.connected').toggleClass('on');
        connected = false;
    });

    // Create a connection to the rosbridge WebSocket server.
    ros.connect('ws://husky.local:9090');
    

//     // Gets called whenever you receive a message for your subscriptions
//     client.onMessageArrived = function (message) {
//         Do something with the push message you received
//         if (receiving) {
//         $('#messages').prepend('<span>Topic: ' + message.destinationName + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data: ' + message.payloadString + '</span><br/>');
//         }
//     };

    //Subscribing to a Topic
    //----------------------

    // Like when publishing a topic, we first create a Topic object with details of the topic's name
    // and message type. Note that we can call publish or subscribe on the same topic object.
//     var listener = new ROSLIB.Topic({
//         ros : ros,
//         name : '/listener',
//         messageType : 'std_msgs/String'
//     });
// 
//       // Then we add a callback to be called every time a message is published on this topic.
//     listener.subscribe(function(message) {
//         console.log('Received message on ' + listener.name + ': ' + message.data);
// 
//         // If desired, we can unsubscribe from the topic as well.
//         listener.unsubscribe();
//     });

      // First, we create a Topic object with details of the topic's name and message type.
    var cmdVel = new ROSLIB.Topic({
        ros : ros,
        name : '/cmd_vel',
        messageType : 'geometry_msgs/Twist'
    });

    // Then we create the payload to be published. The object we pass in to ros.Message matches the
    // fields defined in the geometry_msgs/Twist.msg definition.
    var twist = new ROSLIB.Message({
        linear : {
          x : 0.0,
          y : 0.0,
          z : 0.0
        },
        angular : {
          x : 0.0,
          y : 0.0,
          z : 0.0
        }
    });

    
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


// Publish 10 times per second (100ms)
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
        var twist = new ROSLIB.Message({
        linear : {
          x : vec.y * max_forward / 100.0,
          y : 0.0,
          z : 0.0
        },
        angular : {
          x : 0.0,
          y : 0.0,
          z : -vec.x * max_ang_vel / 100.0
        }
    });
    
    // And finally, publish.
    cmdVel.publish(twist);
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



