#!/usr/bin/env node

var child_process = require('child_process');
var device_id = child_process.execSync('cat /sys/class/net/eth0/address | sed s/://g').toString().replace(/\n$/, '');
process.env['BLENO_DEVICE_NAME'] = 'LAMPI ' + device_id;

var bleno = require('bleno');

var DeviceInfoService = require('./device-info-service');
var deviceInfoService = new DeviceInfoService( 'CWRU', 'LAMPI', device_id);
var LampService = require('./lampi-service');

var LampState = require('./lampi-state');
var lampState = new LampState();
var lampService = new LampService(lampState);

bleno.on('stateChange', function(state) {
  if (state === 'poweredOn') {
    bleno.startAdvertising('MyService', [deviceInfoService.uuid, lampService.uuid], function(err)  {
      if (err) {
        console.log(err);
      }
    });
  }
  else {
    bleno.stopAdvertising();
    console.log('not poweredOn');
  }
});

bleno.on('advertisingStart', function(err) {
  if (!err) {
    console.log('advertising...');
    //
    // Once we are advertising, it's time to set up our services,
    // along with our characteristics.
    //
    bleno.setServices([
        deviceInfoService,
        lampService
    ]);
  }
});
