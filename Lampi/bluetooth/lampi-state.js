var events = require('events');
var util = require('util');
var mqtt = require('mqtt');

function LampiState() {
    events.EventEmitter.call(this);

    this.is_on = true;
    this.brightness = 1.0;
    this.hue = 1.0;
    this.saturation = 1.0;
    var that = this;

    mqtt_client = mqtt.connect('mqtt://localhost');
    mqtt_client.on('connect', function() {
        console.log('connected!');
        mqtt_client.subscribe('lamp/changed');
    });

    mqtt_client.on('message', function(topic, message) {
        new_state = JSON.parse(message);
        if(new_state['client'] != 'bluetooth'){
            console.log('NEW STATE: ', new_state);
            var new_onoff = new_state['on'];
            var new_brightness = Math.round(new_state['brightness']*0xFF);
            var new_hue = Math.round(new_state['color']['h']*0xFF);
            var new_saturation = Math.round(new_state['color']['s']*0xFF);
            if (that.is_on !== new_onoff) {
                console.log('MQTT - NEW ON/OFF');
                that.is_on = new_state['on'];
                that.emit('changed-onoff', that.is_on);
            }
            if (that.brightness !== new_brightness) {
                console.log('MQTT - NEW BRIGHTNESS');
                that.brightness = new_brightness;
                that.emit('changed-brightness', that.brightness);
            }
            if (that.hue !== new_hue) {
                console.log('MQTT - NEW HUE');
                that.hue = new_hue;
                that.emit('changed-hsv', [that.hue, that.saturation]);
            }
            if (that.saturation !== new_saturation) {
                console.log('MQTT - NEW SATURATION');
                that.saturation = new_saturation;
                that.emit('changed-hsv', [that.hue, that.saturation]);
            }
        }

    });

    this.mqtt_client = mqtt_client;
}

util.inherits(LampiState, events.EventEmitter);

LampiState.prototype.set_onoff = function(is_on) {
    this.is_on = is_on;
    var tmp = {'color': {'h':this.hue/255, 's': this.saturation/255}, 'brightness':this.brightness/255, 'on':this.is_on, 'client': 'bluetooth' };
    this.mqtt_client.publish('lamp/set_config', JSON.stringify(tmp));
    console.log('is_on = ', this.is_on);
};

LampiState.prototype.set_brightness = function(brightness){
    this.brightness = brightness;
    var tmp = {'color': {'h':this.hue/255, 's': this.saturation/255}, 'brightness':this.brightness/255, 'on':this.is_on, 'client': 'bluetooth' };
    this.mqtt_client.publish('lamp/set_config', JSON.stringify(tmp));
};

LampiState.prototype.set_hsv = function(color){
    this.hue = color[0];
    this.saturation = color[1];
    var tmp = {'color': {'h':this.hue/255, 's': this.saturation/255}, 'brightness':this.brightness/255, 'on':this.is_on, 'client': 'bluetooth' };
    this.mqtt_client.publish('lamp/set_config', JSON.stringify(tmp));

};
module.exports = LampiState;
