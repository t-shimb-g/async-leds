import network

class Wifi:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.connect(ssid, password)
        
    def connect(self, ssid, password):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            print('connecting to network...')
            wlan.connect(ssid, password)
            while not wlan.isconnected():
                pass
            
        self.wlan = wlan
        
    def get_ip_addr(self):
        return self.wlan.ifconfig()[0]
