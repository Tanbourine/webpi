import RPi.GPIO as GPIO
from flask import Flask, render_template, request

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)

pins = {
        17: {'name': 'out1', 'state': GPIO.LOW},
        27: {'name': 'out2', 'state': GPIO.LOW}
        }

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

@app.route("/")
def main():
    # for each pin, read pin state and store in pins dictionary
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)

    # put pin dictionary into template data dict
    templateData = {
            'pins':pins
            }

    return render_template('main.html', **templateData)

@app.route("/<changePin>/<action>")
def action(changePin, action):
    #convert pin from URL into int
    changePin = int(changePin)
    # get device name for pin being changed:
    deviceName = pins[changePin]['name']
    # if the action part of URL is on, execute code below:
    if action == 'on':
        GPIO.output(changePin, GPIO.HIGH)
        message = "Turned " + deviceName + " on."
    if action == 'off':
        GPIO.output(changePin, GPIO.LOW)
        message = "Turned " + deviceName + " off."
    if action == 'toggle':
        GPIO.output(changePin, not GPIO.input(changePin))
        message = "Toggled " + deviceName + "."


    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)

        templateData = {
                'message' : message,
                'pins' : pins
                }

        return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

