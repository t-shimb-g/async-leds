from machine import Pin, PWM

class RGBLed:
    def __init__(self, pin_numbers):
        self.leds = [PWM(Pin(i, Pin.OUT)) for i in pin_numbers]
        # Assumed pin_numbers correlate to [red, green, blue]
        
    def deinitPWMs(self):
        """Deinitializes the all PWMs"""
        for pwm in self.leds:
            pwm.deinit()
            
    def quadratic_fix(self, value):
        """Fixes the value to scale with how the human eye perceives light"""
        return round(value**2 / (1024 - 1))
        
    def set_color(self, rgb):
        """Takes in a list of 3 values and sets those to each of the 3 LEDs"""
        for i in range(len(self.leds)):
            self.leds[i].duty(1023 - self.quadratic_fix(rgb[i]))
    