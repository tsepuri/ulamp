var util = require('util');
var events = require('events');
var bleno = require('bleno');

var CHARACTERISTIC_NAME = 'Brightness';

function BrightnessCharacteristic(lampi_state){
    bleno.Characteristic.call(this, {
        uuid: '0003A7D3-D8A4-4FEA-8174-1736E808C066',
        properties: ['read','write','notify'],
        descriptors: [
            new bleno.Descriptor({
                uuid: '2901',
                value: CHARACTERISTIC_NAME
            }),
            new bleno.Descriptor({
                uuid: '2904',
                value: new Buffer.from([0x04, 0x00, 0x27, 0x00, 0x01, 0x00, 0x00])
            }),
        ],
    }
    )

    this.lampi_state = lampi_state;

    this._update = null;

    this.changed = function(new_value){
        if (this._update !== null){
            console.log(new_value);
            var data = Buffer.alloc(1);
            data.writeUInt8(new_value, 0);
            this._update(data);
        }
    }

    this.lampi_state.on('changed-brightness', this.changed.bind(this));
}

util.inherits(BrightnessCharacteristic, bleno.Characteristic);

BrightnessCharacteristic.prototype.onReadRequest = function(offset, callback) {
    console.log('onReadRequest');
    if(offset) {
        callback(this.RESULT_ATTR_NOT_LONG, null);
    }
    else {
        var data = new Buffer.alloc(1);
        data.writeUInt8(this.lampi_state.brightness);
        console.log('onReadRequest returning ', data);
        callback(this.RESULT_SUCCESS, data);
        // to cause the value to change, we will create a side-effect here
    }
}

BrightnessCharacteristic.prototype.onWriteRequest = function(data, offset, withoutResponse, callback) {
    if(offset) {
        callback(this.RESULT_ATTR_NOT_LONG);
    }
    else if (data.length !== 1) {
        callback(this.RESULT_INVALID_ATTRIBUTE_LENGTH);
    }
    else {
        var new_value = data.readUInt8(0);
        console.log(new_value);
        this.lampi_state.set_brightness(new_value);
        callback(this.RESULT_SUCCESS);
    }
};

BrightnessCharacteristic.prototype.onSubscribe = function(maxValueSize, updateValueCallback) {
    console.log('subscribe on ', CHARACTERISTIC_NAME);
    this._update = updateValueCallback;
}

BrightnessCharacteristic.prototype.onUnsubscribe = function() {
    console.log('unsubscribe on ', CHARACTERISTIC_NAME);
    this._update = null;
}

module.exports = BrightnessCharacteristic;
