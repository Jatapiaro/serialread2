# -*- coding: utf8 -*-

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Line
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock

import serial
import requests

from kivy.lang import Builder
from kivy.app import App
from kivy.properties import ObjectProperty

Builder.load_file('GUI.kv')

# Basic class Float Layout
class GUI(FloatLayout):

    flag = 0

    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)
        # Set the timer for redrawing the screen
        refresh_time = 5
        Clock.schedule_interval(self.timer, refresh_time)

    def timer(self, dt):
        if self.flag == 0:
            arduino.readline()
            self.flag = 1
        else:
            # Get data from serial port
            value = str(arduino.readline()).replace("\n", "")
            v = float(value)
            self.ids['distance'].text = "[size=50][b]Medición: " + value + "cm[/b][/size]"

            payload = "{\n\t\"measure\": {\n\t\t\"height\": " + value + "\n\t}\n}"
            headers = {
                'content-type': "application/json",
                'cache-control': "no-cache",
                'postman-token': "57acf325-4021-c728-4e75-693c082dc459"
            }

            url = "https://tinacos.herokuapp.com/containers/1/measures.json"
            response = requests.request("POST", url, data=payload, headers=headers)
            water_q = str(response.text.split("water_quantity\":\"")[1].replace("\"}", ""))
            self.ids['response'].text = "[size=50][b]Cantidad de agua: " + water_q + " litros[/b][/size]"
            self.ids['metrics'].text= '[size=20][b]Consulta tus métricas en: https://tinacos.herokuapp.com/containers/1/metrics[/b][/size]'

# Main App class
class SerialDataApp(App):
    def build(self):
        return GUI()

# Main program
if __name__ == '__main__':
    # Connect to serial port first
    try:
        arduino = serial.Serial('/dev/tty.usbmodem1411', 9600)
    except:
        print("Failed to connect")
        exit()

    # Launch the app
    SerialDataApp().run()

    # Close serial communication
    arduino.close()