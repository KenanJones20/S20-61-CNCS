import socket
import selectors
import traceback

import mainlib

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen


class MainWindow(Screen):
    out = StringProperty()

    # pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    sel = selectors.DefaultSelector()
    port = 6600
    host = '192.168.5.1'
    request = ''

    def water_need_request(self):
        self.request = dict(
            type="text/json",
            encoding="utf-8",
            content=dict(action="water", value="need")
        )
        self.out = "Watering needed..."

    def water_all_request(self):
        self.request = dict(
            type="text/json",
            encoding="utf-8",
            content=dict(action="water", value="all")
        )
        self.out = "Watering all..."

    def plant_request(self):
        self.request = dict(
            type="text/json",
            encoding="utf-8",
            content=dict(action="plant"),
        )
        self.out = "Planting..."

    def exit_request(self):
        self.request = dict(
            type="text/json",
            encoding="utf-8",
            content=dict(action="exit"),
        )
        self.out = "Raspberry Pi shutting down..."

    def start_connection(self):
        addr = (self.host, self.port)
        print("starting connection to", addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = mainlib.Message(self.sel, sock, addr, self.request)
        self.sel.register(sock, events, data=message)
        try:
            while True:
                events = self.sel.select(timeout=1)
                for key, mask in events:
                    message = key.data
                    try:
                        message.process_events(mask)
                    except Exception:
                        print(
                            "main: error: exception for",
                            f"{message.addr}:\n{traceback.format_exc()}",
                        )
                        message.close()
                # Check for a socket being monitored to continue.
                if not self.sel.get_map():
                    break
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")
    pass


kv = Builder.load_file("main.kv")
sm = ScreenManager()
sm.add_widget(MainWindow(name="main"))


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
