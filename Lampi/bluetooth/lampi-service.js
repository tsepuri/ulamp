var util = require('util');
var events = require('events');
var bleno = require('bleno');
var OnOffCharacteristic = require('./lampi-onoff-characteristic');
var BrightnessCharacteristic = require('./lampi-brightness-characteristic');
var HSVCharacteristic = require('./lampi-hsv-characteristic');

function LampService(lampi_state) {
    bleno.PrimaryService.call(this, {
        uuid: '0001A7D3-D8A4-4FEA-8174-1736E808C066',
        characteristics: [
            new OnOffCharacteristic(lampi_state),
            new BrightnessCharacteristic(lampi_state),
            new HSVCharacteristic(lampi_state),
        ]
    });
}

util.inherits(LampService, bleno.PrimaryService);

module.exports = LampService;
