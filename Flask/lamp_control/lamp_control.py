import time
from itertools import cycle
from flask import Flask, render_template
# from robot_brain.gpio_pin import GPIOPin

app = Flask(__name__)
state_cycle = cycle(['on', 'off'])
# locations = {
#     'bedroom': (GPIOPin(24), GPIOPin(25)),
#     'porch': (GPIOPin(18), GPIOPin(23)),
# }

@app.route("/")
@app.route("/<state>")
@app.route("/<location>/<state>")
def update_lamp(location='porch', state=None):
    if state == 'on':
#         locations[location][0].set(1)
        time.sleep(.2)
#         locations[location][0].set(0)
    if state == 'off':
#         locations[location][1].set(1)
        time.sleep(.2)
#         locations[location][1].set(0)
    if state == 'toggle':
        state = next(state_cycle)
        update_lamp(state)
    template_data = {
        'title' : state,
        'location': location,
    }
    return render_template('main.html', **template_data)

if __name__ == "__main__":
    app.run(debug=True)
