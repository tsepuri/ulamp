//
//  Lampi.swift
//  Lampi
//

import Foundation
import SwiftUI

class Lampi: ObservableObject {
    @Published var hue: Double = 1.0
    @Published var saturation: Double = 1.0
    @Published var brightness: Double = 1.0

    @Published var isOn = false

    var color: Color {
        Color(hue: hue, saturation: saturation, brightness: brightness)
    }

    var baseHueColor: Color {
        Color(hue: hue, saturation: 1.0, brightness: 1.0)
    }
}
