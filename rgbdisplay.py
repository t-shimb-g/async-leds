from machine import Pin, SoftI2C
import ssd1306 # display driver

class RGBDisplay:    
    def __init__(self, sda, scl, width, height):
        # an i2c object for communicating using these two pins
        self.i2c = SoftI2C(sda=Pin(sda), scl=Pin(scl))
        self.display = ssd1306.SSD1306_I2C(width, height, self.i2c)
    
    def clear_values(self):
        """Fills only the left side of the screen where the labels are displayed"""
        self.display.rect(43, 16, 100, 64, 0, 1)
        
    def clear_labels(self):
        """Fills only the right side of the screen where the values are displayed"""
        
        self.display.rect(0, 16, 45, 64, 0, 1)
        
    def refresh(self):
        """Runs the loop functions that fill the display with info"""
        
        self.label_loop()
        self.value_loop()
        self.display.show()
        
    def display_setup(self, line_count, colors, values):
        """Initial run and cache of values used throughout the object"""
        
        # Cache the values for use elsewhere in the object
        self.values_cache = values
        self.colors_cache = colors
        self.line_count_cache = line_count
        
        self.display.text('RGB LED Settings', 0, 0, 1)
        
        # Setup display
        self.refresh()
        
    def update_values(self, values):
        self.values_cache = values
        
    def label(self, line, color):
        self.display.text(color, 4, (line+1)*11, 1) # Displays rgb label
        
    def label_loop(self):
        """Loop that displays all of the labels in `self.colors_cache` using `self.line()`"""
        
        self.clear_labels()
        
        for i in range(self.line_count_cache):
            self.label(i + 1, self.colors_cache[i])
                
        
    def value(self, line, value):
        self.display.rect(46, (line+1)*11, round((value/1024)*80), 8, 1, 1) # Displays rgb value
        
    def value_loop(self):
        """Loop that displays all of the values in `self.values_cache` using `self.value()`"""
        
        self.clear_values()
        
        for i in range(self.line_count_cache - 1):
            self.value(i + 1, self.values_cache[i])
        
    def line_select(self, line):
        """Provides visual to show user with label they are 'hovering' over"""
        
        self.clear_labels()
        self.label_loop()        
        self.display.rect(4, ((line+2)*11)-2, 40, 11, 1, 0) # Rectangle to show user's `cursor`
        self.display.show()
        
    def show_selected(self, line):
        """Changes display of the selected label to show selection state"""
        
        if line < 0:
            return
        
        self.display.rect(4, ((line+2)*11)-2, 40, 11, 1, 1) # Fill in selection rectangle
        self.display.text(self.colors_cache[line], 4, (line+2)*11, 0) # Invert label under rectangle
        self.display.show()
        