// SocketIO functions when the document is ready
$(document).ready(function(){
    vec = Object.seal({
    x: 0,
    y: 0
    });

    namespace = '/CRAWLAB'; // change to an empty string to use the global namespace

    // the socket.io documentation recommends sending an explicit package upon connection
    // this is specially important when using the global namespace
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    socket.on('connect', function() {
        socket.emit('my event', {data: 'I\'m connected!'});
    });

    // event handler for server sent data
    // the data is displayed in the "Received" section of the page
    socket.on('my response', function(msg) {
        $('#log').append('<br>Received #' + msg.count + ': ' + msg.data);
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
    
    
    
    // Send the data over a websocket 10 times per second (100ms)
    (function send_data_at_interval() {
        socket.emit('my broadcast event', {data: dpad});
        setTimeout(send_data_at_interval, 100);
        })();  

});

 


