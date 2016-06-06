// SocketIO functions when the document is ready
$(document).ready(function(){

    namespace = '/CRAWLAB'; // change to an empty string to use the global namespace

    // the socket.io documentation recommends sending an explicit package upon connection
    // this is specially important when using the global namespace
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    
    socket.on('connect', function() {
        socket.emit('my event', {data: 'Connected.'});
    });

    // event handler for server sent data
    // the data is displayed in the "Received" section of the page
    socket.on('my response', function(msg) {
        $('#log').append('<br>Received #' + msg.count + ': ' + msg.data);
    });

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

//             $('.connected').toggleClass('on', false);
//             $('.sending').toggleClass('on', false);
//             $('.subscribed').toggleClass('on', false);
//             $('.receiving').toggleClass('on', false);
//             $('#receive').text('Receive');
//             $('#control').text('Start');
            

    
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


    // Send the data over a websocket 10 times per second (100ms)
    (function send_data_at_interval() {
        socket.emit('my broadcast event', {data: vec});
        setTimeout(send_data_at_interval, 100);
        console.log(vec)
        })();  
        
        
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


