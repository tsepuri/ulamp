//
//  LampiApp.swift
//  Lampi
//

import SwiftUI
import Mixpanel

@main
struct LampiApp: App {
    let DEVICE_NAME = "LAMPI b827eb07eae8"
    
    let MIXPANEL_TOKEN = "416b189bda798db7d192ff24f657399a"

    let USE_BROWSER = false
    
    init() {
            Mixpanel.initialize(token: MIXPANEL_TOKEN)
            Mixpanel.mainInstance().registerSuperProperties(["interface": "iOS"])
    }
    var body: some Scene {
        WindowGroup {
            if USE_BROWSER {
                LampiBrowserView()
            } else {
                LampiView(lamp: Lampi(name: DEVICE_NAME))
            }
        }
    }
}
extension MixpanelInstance {
    func trackUIEvent(_ event: String?, properties: Properties = [:]) {
        var eventProperties = properties
        eventProperties["event_type"] = "ui"

        track(event: event, properties: eventProperties)
    }
}
