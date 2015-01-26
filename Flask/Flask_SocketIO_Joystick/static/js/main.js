// SocketIO functions when the document is ready
$(document).ready(function(){
    vec = Object.seal({
    x: 0,
    y: 0
    });

    namespace = '/test'; // change to an empty string to use the global namespace

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
    
    tester = $('#tester');
tester.draggable();

JoyStick('#joystick1', 120, function(magnitude, theta, ximpulse, yimpulse) {
    vec.x = ximpulse;
    vec.y = yimpulse;
    
    console.log(vec.x, vec.y)
    
    // Limit output to between -100 and 100
    if (vec.x > 100){
        vec.x = 100;
    }
    else if (vec.x < -100){
        vec.x = -100;
    }
    
    if (vec.y > 100){
        vec.y = 100;
    }
    else if (vec.y < -100){
        vec.y = -100;
    }
});

// Send the data over a websocket 10 times per second (1000/100)
iid = setInterval(function() {
    // Emit the data over the websocket
    socket.emit('my broadcast event', {data: [vec.x, vec.y]});}, 10);
});
