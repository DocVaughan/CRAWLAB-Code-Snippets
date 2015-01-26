$(window).load(function(){
vec = Object.seal({
    x: 0,
    y: 0
});

tester = $('#tester');
tester.draggable();

JoyStick('#joystick1', 120, function(magnitude, theta, ximpulse, yimpulse) {
    //console.log(magnitude, theta, ximpulse, yimpulse);
    vec.x = 10 * (ximpulse / 80);
    vec.y = 10 * (yimpulse / 80);
});

iid = setInterval(function() {
    //console.log(vec, tester.css('top'), tester.css('left'));
    tester.css('top', (parseInt(tester.css('top').substr(0, tester.css('top').length - 2), 10) - vec.y) + 'px');
    tester.css('left', (parseInt(tester.css('left').substr(0, tester.css('left').length - 2), 10) + vec.x) + 'px');
}, 1000 / 60);

});