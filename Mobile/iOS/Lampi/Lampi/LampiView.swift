//
//  ContentView.swift
//  Lampi
//
//  Created by Tarun  on 3/17/22.
//

import SwiftUI

class Lampi: ObservableObject {
    @Published var hue: Double = 1.0
    @Published var saturation: Double = 1.0
    @Published var brightness: Double = 1.0
    @Published var power: Bool = true
    var color: Color {
        Color(hue: hue, saturation: saturation, brightness: brightness)
    }
}

struct LampiView: View {
    @ObservedObject var lampi = Lampi()
    var body: some View {
        VStack {
            Rectangle()
                    .fill(lampi.color)
                    .edgesIgnoringSafeArea([.top])
                GradientSlider(value: $lampi.hue,
                               handleColor: Color(hue: lampi.hue, saturation: 1.0, brightness: 1.0),
                               trackColors: [.red, .yellow, .green, .cyan, .blue,
                        .purple, .red])
                    .padding()
                GradientSlider(value: $lampi.saturation,
                               handleColor: Color(hue: lampi.hue, saturation: lampi.saturation, brightness: 1.0),
                               trackColors: [.white, Color(hue: lampi.hue, saturation: 1.0, brightness: 1.0)])
                    .padding()
                GradientSlider(value: $lampi.brightness,
                               handleColor: Color(hue: 1.0, saturation: 0.0, brightness: lampi.brightness),handleImage: Image(systemName: "sun.max")
                                                                                                                                , trackColors: [.black, .white])
                .foregroundColor(Color(hue: 1.0, saturation: 0.0, brightness: abs(1 - lampi.brightness)))
                    .padding()
            Button(action: {
                lampi.power = !lampi.power
                        }){
                            HStack{
                                Spacer()
                                Image(systemName: "power")
                                    .resizable()
                                    .aspectRatio(contentMode: .fit)
                                Spacer()
                            }.padding()
                        }
                        .frame(height: 80)
                        .foregroundColor(lampi.color)
                        .background(.black)
                
            }
        }
}

struct LampiView_Previews: PreviewProvider {
    static var previews: some View {
        LampiView()
    }
}
