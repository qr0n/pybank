from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from plyer import battery
import json
import httpx


###functions.py###
class batt():
    @staticmethod
    def is_charging():
        while battery.status["isCharging"] == True:
            return "Yes"
        while battery.status["isCharging"] == False:
            return "No"

class inet:
    def upload():
        # req = UrlRequest(f"https://pbcfg.qr0n.repl.co/download")
        unloaded = httpx.get("https://pbcfg.qr0n.repl.co/").text
        req = json.loads(unloaded)
        return req["percent"]

Builder.load_string('''
<BatteryInterface>:
    lbl1: lbl1
    lbl2: lbl2
    BoxLayout:
        orientation: 'vertical'

        Label:
            text: "Is Charging?"
            
        Label:
            id: lbl1
            text: "Getting Status"
            
        Label:
            text: "Percentage"
            
        Label:
            id: lbl2
            text: "Getting Percentage"
        
            
''')

    
class BatteryInterface(BoxLayout):
    lbl1 = ObjectProperty()
    lbl2 = ObjectProperty()

    # def get_status(self, *args):
    #     self.lbl1.text = batt.is_charging()
    #     self.lbl2.text = str(battery.status['percentage']) + "%"
    
    def set_label(self, dt):
            self.ids.lbl1.text = batt.is_charging()
            self.lbl2.text = str(battery.status["percentage"]) + "%"
    
    def get_battery(self, dt):
        UrlRequest(f"https://pbcfg.qr0n.repl.co/upload?p={battery.status['percentage']}&d=world")


class BatteryApp(App):
    def build(self):
        ui = BatteryInterface()
        Clock.schedule_interval(ui.set_label, .1)
        try:
            Clock.schedule_interval(ui.get_battery, 10)
        except Exception as E:
            pass
        return ui

    def on_pause(self):
        return True
    

app = BatteryApp()
app.run()
