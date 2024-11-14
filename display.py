from machine import Pin, SoftI2C
from rgbdisplay import RGBDisplay
import ssd1306
    

class Display:
    def __init__(self, sda, scl):
        i2c = SoftI2C(sda=Pin(sda), scl=Pin(scl))
        self.buffer = ssd1306.SSD1306_I2C(128, 64, i2c)
        
        self.rgb_display = RGBDisplay(sda, scl, 128, 64)
        self.clear()
        self.show()
        
    def ipaddr(self, ip, port):
        self.ip_cache = ip
        self.port_cache = port
        
        self.buffer.text(f'{ip}', 0, 0)
        self.buffer.text(f'port {port}', 0, 8)
        
    def led_info(self, percentage):
        # heading
        self.buffer.text('LED Controller', 0, 20)
        
        # slider
        self.buffer.rect(0, 32, 90, 8, 1, False)
        scaled = (90*percentage) // 100
        self.buffer.rect(2, 34, scaled-4, 4, 1, True)
        
        # percentage
        self.buffer.text(f'{percentage}%', 94, 32)
        
    def led_rooms(self, led_bools):
        width = 48
        height = 22
        
        self.clear()
        
        self.buffer.rect(14, 16, width, height, 1, False)
        self.buffer.text('RGB', 26, 23, True)
        
        self.buffer.rect(66, 16, width, height, 1, led_bools[1])
        self.buffer.text('Red', 78, 23, not led_bools[1])
        
        self.buffer.rect(14, 40, width, height, 1, led_bools[2])
        self.buffer.text('Green', 18, 47, not led_bools[2])
        
        self.buffer.rect(66, 40, width, height, 1, led_bools[3])
        self.buffer.text('Blue', 74, 47, not led_bools[3])
        
    def rgb_selection(self, labels, values):
        self.labels_cache = labels
        self.values_cache = values
        
        self.buffer.fill(0)
        self.ipaddr(self.ip_cache, self.port_cache)
        self.rgb_display.display_setup(4, self.labels_cache, self.values_cache)
        self.rgb_display.line_select(0)
        
        
    def show(self):
        self.buffer.show()
        
    def clear(self):
        """Clear everything below 16 pixels of yellow"""
        self.buffer.rect(0, 16, 128, 48, 0, True)