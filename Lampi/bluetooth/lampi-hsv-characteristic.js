var util = require('util');
var events = require('events');
var bleno = require('bleno');

var CHARACTERISTIC_NAME = 'HSV';

function HSVCharacteristic(lampi_state){
    bleno.Characteristic.call(this, {
        uuid: '0002A7D3-D8A4-4FEA-8174-1736E808C066',
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
            var data = Buffer.alloc(3);
            data.writeUInt8(new_value[0], 0);
            data.writeUInt8(new_value[1], 1);
            data.writeUInt8(255, 2);
            this._update(data);
        }
    }

    this.lampi_state.on('changed-hsv', this.changed.bind(this));
}

util.inherits(HSVCharacteristic, bleno.Characteristic);

HSVCharacteristic.prototype.onReadRequest = function(offset, callback) {
    console.log('onReadRequest');
    if(offset) {
        callback(this.RESULT_ATTR_NOT_LONG, null);
    }
    else {
        var data = new Buffer.alloc(3);
        data.writeUInt8(this.lampi_state.hue);
        data.writeUInt8(this.lampi_state.saturation, 1);
        data.writeUInt8(255, 2);
        console.log('onReadRequest returning ', data);
        callback(this.RESULT_SUCCESS, data);
        // to cause the value to change, we will create a side-effect here
    }
}

HSVCharacteristic.prototype.onWriteRequest = function(data, offset, withoutResponse, callback) {
    if(offset) {
        callback(this.RESULT_ATTR_NOT_LONG);
    }
    else if (data.length !== 3) {
        callback(this.RESULT_INVALID_ATTRIBUTE_LENGTH);
    }
    else {
        var new_hue = data.readUInt8(0);
        var new_saturation = data.readUInt8(1);
        var new_value = data.readUInt8(2);
        console.log('val ', new_value);
        if(new_value != 255){
            callback(this.RESULT_INVALID_ATTRIBUTE_LENGTH);
        }
        else{
            console.log(new_value);
            this.lampi_state.set_hsv([new_hue, new_saturation, new_value]);
            callback(this.RESULT_SUCCESS);
        }
    }
};

HSVCharacteristic.prototype.onSubscribe = function(maxValueSize, updateValueCallback) {
    console.log('subscribe on ', CHARACTERISTIC_NAME);
    this._update = updateValueCallback;
}

HSVCharacteristic.prototype.onUnsubscribe = function() {
    console.log('unsubscribe on ', CHARACTERISTIC_NAME);
    this._update = null;
}

module.exports = HSVCharacteristic;
