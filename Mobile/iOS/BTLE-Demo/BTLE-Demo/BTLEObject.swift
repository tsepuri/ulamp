//
//  BTLEObject.swift
//  EECS397-iOS-Demo
//

import Foundation
import CoreBluetooth

class BTLEObject: ObservableObject {
    @Published var number: Double = 0.0
    
    private var bluetoothManager: CBCentralManager!
}
