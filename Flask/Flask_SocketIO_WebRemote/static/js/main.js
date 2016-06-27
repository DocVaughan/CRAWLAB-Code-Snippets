// SocketIO functions when the document is ready
$(document).ready(function(){

    // Time variables
    var date = new Date();
    var start_Time = date.getTime();
    var time_elapsed = date.getTime() - start_Time;

    namespace = '/CRAWLAB'; // change to an empty string to use the global namespace

    // the socket.io documentation recommends sending an explicit package upon connection
    // this is specially important when using the global namespace
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    
    socket.on('connect', function() {
        socket.emit('connections', {data: 'Connected.'});
        $('.connected').toggleClass('on');
        connected = false;
    });

    socket.on('disconnect', function () {
        socket.emit('Disconnected');
        $('.connected').toggleClass('on');
        connected = false;
    });


    // Functions for the draggable joystick - implemented in Joystick.js
    vec = Object.seal({
    x: 0,
    y: 0
    });

    // Chartjs livestreaming setup and exectution
    var x_received = 0;
    var y_received = 0;
    var dps_x = [];         // dataPoints
    var dps_y = [];         // dataPoints
    var dataLength = 100;   // number of dataPoints visible at any point

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
            interval: 1,
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

    // Set up and process the joystick object
    JoyStick('#joystick1', 120, function(magnitude, theta, ximpulse, yimpulse) {
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

//     socket.on('sensor_data', function(message){
//         
//     }


    // event handler for server sent data
    // the data is displayed in the "Received" section of the page and plotted
    socket.on('sensor_data', function(msg) {
        if (receiving) {
            $('#messages').prepend('Received ' + msg['data_x'] + ', ' + msg['data_y'] + '<br>');
            x_received = msg['data_x'];
            y_received = msg['data_y'];
            time_elapsed = (new Date() - start_Time) / 1000;
            updateChart();
        }
    });
    
    
    // handlers for the different forms in the page
    // these send data to the server in a variety of ways
    $('form#emit').submit(function(event) {
        socket.emit('my event', {data: $('#emit_data').val()});
        return false;
    });
    $('form#broadcast').submit(function(event) {
        socket.emit('my broadcast event', {data: $('#broadcast_data').val()});
        return false;
    });
    $('form#join').submit(function(event) {
        socket.emit('join', {room: $('#join_room').val()});
        return false;
    });
    $('form#leave').submit(function(event) {
        socket.emit('leave', {room: $('#leave_room').val()});
        return false;
    });
    $('form#send_room').submit(function(event) {
        socket.emit('my room event', {room: $('#room_name').val(), data: $('#room_data').val()});
        return false;
    });
    $('form#close').submit(function(event) {
        socket.emit('close room', {room: $('#close_room').val()});
        return false;
    });
    $('form#disconnect').submit(function(event) {
        socket.emit('disconnect request');
        return false;
    });

    // Read and send the Dpad button states over websocket
    var timeout_up = $('#up');
    var timeout_down = $('#down');
    var timeout_right = $('#right');
    var timeout_left = $('#left'); 
    var sending = false;  
    var receiving = false;   
    var subscribed = false;
    var connected = false;

//     $('.connected').toggleClass('on', false);
//     $('.sending').toggleClass('on', false);
//     $('.subscribed').toggleClass('on', false);
//     $('.receiving').toggleClass('on', false);
//     $('#receive').text('Receive');
//     $('#control').text('Start');
            

    
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

//     // Send the data over a websocket 10 times per second (100ms)
//     (function send_data_at_interval() {
//         socket.emit('velocity_commands', {data: vec});
//         setTimeout(send_data_at_interval, 100);
//         console.log(vec)
//         })();  
        
        
    // Send the data over websockets 10 times per second (100ms)
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
        socket.emit('velocity_commands', {vel: vec});
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
            $("#receive").text('Stop');
            receiving = true;
            $('.receiving').toggleClass('on');
            $('#messages').text('');
        }
    };
    
        
    $('.exit_button').mousedown(function (){
        socket.emit('my broadcast event', {data: 'exit'});
        });
        
        
        

$(function navigation() {
	   // To make dropdown actually work
	   // To make more unobtrusive: http://css-tricks.com/4064-unobtrusive-page-changer/
      $("nav select").change(function() {
        window.location = $(this).find("option:selected").val();
      }); 
    });

});


