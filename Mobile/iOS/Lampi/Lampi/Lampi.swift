//
//  Lampi.swift
//  Lampi
//

import Foundation
import CoreBluetooth
import SwiftUI

class Lampi: NSObject, ObservableObject {
    @Published var state: State = State(){
        didSet {
            if !updatePending && !skipNextWrite {
                if state.hue != oldValue.hue || state.saturation != oldValue.saturation,
                       let hsvCharacteristic = hsvCharacteristic {
                        updatePending = true
                        DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) { [weak self] in
                            guard let self = self else { return }
                            
                            var hsv: UInt32 = 0
                            let hueInt = UInt32(self.state.hue * 255.0)
                            let satInt = UInt32(self.state.saturation * 255.0)
                            let valueInt = UInt32(255)

                            hsv = hueInt
                            hsv += satInt << 8
                            hsv += valueInt << 16

                            let data = Data(bytes: &hsv, count: 3)
                            self.devicePeripheral?.writeValue(data, for: hsvCharacteristic, type: .withResponse)

                            self.updatePending = false

                            print("Updated hsv characteristic over bluetooth")
                        }
                    }
                if state.brightness != oldValue.brightness,
                    let brightnessCharacteristic = brightnessCharacteristic{
                        updatePending = true
                        DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) { [weak self] in
                            guard let self = self else {return}
                            
                            var intToWrite = UInt8(self.state.brightness * 255.0)
                            let dataToWrite = Data(bytes: &intToWrite, count: 1)
                            
                            self.devicePeripheral?.writeValue(dataToWrite, for: brightnessCharacteristic, type: .withResponse)
                            
                            self.updatePending = false
                            
                            print("Updated Brightness characteristic over bluetooth")
                        }
                    }
                if state.isOn != oldValue.isOn,
                    let onOffCharacteristic = onOffCharacteristic{
                        updatePending = true
                        DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) { [weak self] in
                            guard let self = self else {return}
                            
                            var intToWrite = UInt8(self.state.isOn ? 1 : 0)
                            let dataToWrite = Data(bytes: &intToWrite, count: 1)
                            
                            self.devicePeripheral?.writeValue(dataToWrite, for: onOffCharacteristic, type: .withResponse)
                            
                            self.updatePending = false
                            
                            print("Updated On/Off characteristic over bluetooth")
                        }
                    }
                }
                skipNextWrite = false
                }
    }

    var color: Color {
        Color(hue: state.hue, saturation: state.saturation, brightness: state.brightness)
    }

    var baseHueColor: Color {
        Color(hue: state.hue, saturation: 1.0, brightness: 1.0)
    }
    private var bluetoothManager: CBCentralManager!
    private var devicePeripheral: CBPeripheral?
    private var hsvCharacteristic: CBCharacteristic?
    private var brightnessCharacteristic: CBCharacteristic?
    private var onOffCharacteristic: CBCharacteristic?
    private var updatePending: Bool = false
    private var skipNextWrite: Bool = false

    // guard let value = hsvCharacteristic.value else { return }

    override init() {
        super.init()
        self.bluetoothManager = CBCentralManager(delegate: self, queue: nil)
    }
}
extension Lampi: CBCentralManagerDelegate {
    private static let DEVICE_NAME = "LAMPI b827eb07eae8"
    private static let OUR_SERVICE_UUID = "0001A7D3-D8A4-4FEA-8174-1736E808C066"
    func centralManagerDidUpdateState(_ central: CBCentralManager) {
            if central.state == .poweredOn {
                let services = [CBUUID(string:Lampi.OUR_SERVICE_UUID)]
                bluetoothManager.scanForPeripherals(withServices: services)
            }
    }
    func centralManager(_ central: CBCentralManager,
                            didDiscover peripheral: CBPeripheral,
                            advertisementData: [String : Any],
                            rssi RSSI: NSNumber) {
            print("Test")
            if peripheral.name == Lampi.DEVICE_NAME {
                print("Found \(Lampi.DEVICE_NAME)")

                devicePeripheral = peripheral

                bluetoothManager.stopScan()
                bluetoothManager.connect(peripheral)
            }
    }

    func centralManager(_ central: CBCentralManager, didConnect peripheral: CBPeripheral) {
        print("Connected to peripheral: \(peripheral)")
        state.isConnected = true
        peripheral.delegate = self
        peripheral.discoverServices([CBUUID(string:Lampi.OUR_SERVICE_UUID)])
    }

    func centralManager(_ central: CBCentralManager, didDisconnectPeripheral peripheral: CBPeripheral, error: Error?) {
        print("Disconnected from peripheral: \(peripheral)")
        state.isConnected = false
        if central.state == .poweredOn {
            let services = [CBUUID(string:Lampi.OUR_SERVICE_UUID)]
            bluetoothManager.scanForPeripherals(withServices: services)
        }
    }
}
extension Lampi {
    struct State: Equatable {
        var hue: Double = 1.0
        var saturation: Double = 1.0
        var brightness: Double = 1.0
        var isOn: Bool = false
        var isConnected: Bool = false
    }
}
extension Lampi: CBPeripheralDelegate {
    static let HSV_UUID = "0002A7D3-D8A4-4FEA-8174-1736E808C066"
    static let BRIGHTNESS_UUID = "0003A7D3-D8A4-4FEA-8174-1736E808C066"
    static let ONOFF_UUID = "0004A7D3-D8A4-4FEA-8174-1736E808C066"
    func peripheral(_ peripheral: CBPeripheral, didDiscoverServices error: Error?) {
            guard let services = peripheral.services else { return }

            for service in services {
                print("Discovered device service")
                peripheral.discoverCharacteristics(nil, for: service)
            }
    }

    func peripheral(_ peripheral: CBPeripheral, didDiscoverCharacteristicsFor service: CBService, error: Error?) {
            guard let characteristics = service.characteristics else { return }

            for characteristic in characteristics {
                if characteristic.uuid == CBUUID(string: Lampi.HSV_UUID) {
                    print("Found characteristic with UUID: \(Lampi.HSV_UUID)")
                    hsvCharacteristic = characteristic
                    devicePeripheral?.readValue(for: characteristic)
                    devicePeripheral?.setNotifyValue(true, for: characteristic)

            }
            else if characteristic.uuid == CBUUID(string: Lampi.BRIGHTNESS_UUID) {
                    print("Found characteristic with UUID: \(Lampi.BRIGHTNESS_UUID)")
                    brightnessCharacteristic = characteristic
                    devicePeripheral?.readValue(for: characteristic)
                    devicePeripheral?.setNotifyValue(true, for: characteristic)
                }
                else if characteristic.uuid == CBUUID(string: Lampi.ONOFF_UUID) {
                    print("Found characteristic with UUID: \(Lampi.ONOFF_UUID)")
                        onOffCharacteristic = characteristic
                        devicePeripheral?.readValue(for: characteristic)
                        devicePeripheral?.setNotifyValue(true, for: characteristic)
                }
        }
    }
    func peripheral(_ peripheral: CBPeripheral, didUpdateValueFor characteristic: CBCharacteristic, error: Error?) {
        print("Value updated for characteristic with UUID: \(characteristic.uuid)")
        if characteristic == hsvCharacteristic,
           let hsvData = hsvCharacteristic?.value {
           var newHSV = state
            newHSV.hue = Double(hsvData[0]) / 255.0
            newHSV.saturation = Double(hsvData[1]) / 255.0
            skipNextWrite = true
            state = newHSV
        }
        else if characteristic == brightnessCharacteristic,
           let brightnessData = brightnessCharacteristic?.value {
            let newBrightness = Double(brightnessData[0]) / 255.0
            skipNextWrite = true
            state.brightness = newBrightness
        }
        else if characteristic == onOffCharacteristic,
           let onOffData = onOffCharacteristic?.value {
           let newIsOn = onOffData[0] != 0
            skipNextWrite = true
            state.isOn = newIsOn
        }
    }
}

