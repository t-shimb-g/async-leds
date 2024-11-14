from machine import Pin, Timer
from micropython import schedule

class DebouncedSwitch:
    """Tolerates mechanical vibrations of a switch and calls the given
    callback after the switch has settled down.
    
    """
    def __init__(self, pin_num, callback, delay=50, timer_id=0):
        self.pin = Pin(pin_num, Pin.IN)
        self.callback = callback
        self.delay = delay
        
        self.timer = Timer(timer_id)
        self.timer.deinit()
        
        # 1. recognize first button press
        self.pin.irq(self.start_timer, trigger=Pin.IRQ_FALLING)
        
    def start_timer(self, pin):
        self.pin.irq(None) # disable irq to ignore any bounces
        # 2. Set up waiting period
        self.timer.init(period=self.delay, callback=self.timer_wakeup)
        
    def timer_wakeup(self, timer):
        # 3. Wake up and check if
        timer.deinit() # stop timer
        if not self.pin.value(): # true if stabilized
            # 4. Call handler once (we must use schedule to call our function if within an irq)
            schedule(self.callback, self.pin)
            
        # 5. Go back to step 1
        self.pin.irq(self.start_timer, trigger=Pin.IRQ_FALLING)
