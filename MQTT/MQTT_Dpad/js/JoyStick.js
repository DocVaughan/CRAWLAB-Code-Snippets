/*
 * The MIT License (MIT)
 * 
 * Copyright (c) 2014 Invisiball
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

var JoyStick = function(selector, sqhw, done) {
    if (typeof(done) !== 'function') {
        done = function(){};
    }
    
    var container = $(selector);
    var stick = $('<div class="joysticki"></div>');
    var circle = $('<div class="joystickc"></div>');
    
    container.css('width', sqhw + 'px');
    container.css('height', sqhw + 'px');
    container.css('border-radius', (sqhw / 2) + 'px');
    
    stick.css('width', (sqhw / 2) + 'px');
    stick.css('height', (sqhw / 2) + 'px');
    stick.css('top', 'calc( 50% - ' + ((sqhw / 4) + 1) + 'px )');
    stick.css('left', 'calc( 50% - ' + ((sqhw / 4) + 1) + 'px )');
    stick.css('border-radius', sqhw / 8 + 'px');
    
    container.append(circle);
    container.append(stick);

    stick.draggable({
        start: null,
        drag: function() {
            var y = parseInt(this.style.top.substr(0, this.style.top.length - 2), 10) + sqhw / 4;
            var x = parseInt(this.style.left.substr(0, this.style.left.length - 2), 10) + sqhw / 4;
            
//             console.log(x, y);

            
            if (x > sqhw / 2) {
                x -= sqhw / 2;
            } else if (x < sqhw / 2) {
                x = - (sqhw / 2 - x);
            } else {
                x = 0;
            }
            
            if (y > sqhw / 2) {
                y -= sqhw / 2;
            } else if (y < sqhw / 2) {
                y = - (sqhw / 2 - y);
            } else {
                y = 0;
            }
            
            y *= -1;
            
            //console.log(x, y);
            
            var theta = (Math.atan(y / x) || 0) * (180 / Math.PI);
            
            if (x === 0 && y === 0) {
                return done(0, 0, 0, 0);
            }
            
            if (x > 0) {
                if (y <= 0) {
                    theta += 360;
                }
            } else if (x < 0) {
                theta += 180;
            }
            
            var magnitude = Math.sqrt((Math.pow(x, 2) + Math.pow(y, 2)));
            
            if (magnitude > sqhw / 2) {
                magnitude = sqhw / 2;
            }
            
            done(magnitude, theta, x, y);
        },
        stop: function() {
            this.style.top = 'calc( 50% - ' + ((sqhw / 4) + 1) + 'px )';
            this.style.left = 'calc( 50% - ' + ((sqhw / 4) + 1) + 'px )';
            
            done(0, 0, 0, 0);
        }
    });
};
