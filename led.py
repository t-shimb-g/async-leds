from machine import Pin, PWM

class LED:
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin))
        self.pwm.duty(0)
        
    def value(self, value):
        if value:
            self.pwm.duty(1023)
        else:
            self.pwm.duty(0)
        '''
        if percentage is None:
            return round(100 - (100*self.pwm.duty() / 1023))
        
        # clamp between [0..100]
        percentage = min(max(0, percentage), 100)
        
        # compute duty cycle value
        value = round(1023 * percentage / 100)
        self.pwm.duty(1023 - value)
        '''
            
        