import asyncio
import microdot
import json
import time
from machine import ADC, Pin
from websocket import with_websocket
from wifi import Wifi
from display import Display
from rotary_encoder import RotaryEncoder
from debounced_switch import DebouncedSwitch
from rgbled import RGBLed
from led import LED

port = 8080
wifi = Wifi('WarriorNET', 'VictorEWarrior2023')
led_values = [[0, 0, 0], False, False, False]

# Screen setup
display = Display(23, 22)
display.ipaddr(wifi.get_ip_addr(), port)
display.led_rooms(led_values)
display.buffer.rect(16, 18, 44, 18, 1, False)
display.show()

rgb_pins = (15, 2, 0)
RGB_LED = RGBLed(rgb_pins)
RGB_LED.set_color([0, 0, 0])

led_pins = (25, 13, 26)
leds = [LED(i) for i in led_pins]

box_select = 0
x_y_pair = [(16, 18), (68, 18), (16, 42), (68, 42)]

app = microdot.Microdot()

selected_line = 0
state_bool = True

values = [0, 0, 0]
LABELS = ('Red', 'Green', 'Blue', 'Back')

@app.route('/')
async def index(request):
    ipaddr = wifi.get_ip_addr()
    with open('index.html', 'r') as f:
        text = f.read().replace('ADDRESS', f'{ipaddr}:{port}')
        return text, {'Content-Type': 'text/html'}

@app.route('/slider')
@with_websocket
async def slider(request, ws):
    global values
    
    def swap_state(pin):
        """Changes the rotary encoder's interrupt function based on a boolean
        representing which 'state' it is in. The boolean is swapped each time it is ran"""
        
        global state_bool
        global selected_line
        global box_select
        
        if selected_line % 4 == 3:
            box_select = 0
            display.led_rooms(led_values)
            display.buffer.rect(16, 18, 44, 18, 1, False)
            display.show()
            state_bool = not state_bool
            rotary.callback = box_scroll
            switch.callback = select
        elif state_bool:
            display.rgb_display.show_selected(selected_line % 4)
            rotary.callback = change_color
        elif not state_bool:
            display.rgb_display.refresh()
            display.rgb_display.line_select(selected_line)
            rotary.callback = select_color
        
        state_bool = not state_bool

    def change_color(value):
        """Modifies the value selected LED"""
        
        global selected_line
        selected_line %= 4
        
        values[selected_line] += value * 75

        if values[selected_line] <= 0:
            values[selected_line] = 0
        elif values[selected_line] >= 1023:
            values[selected_line] = 1023
        
        display.rgb_display.update_values(values)
        display.rgb_display.value_loop()
        display.rgb_display.show_selected(selected_line)
        RGB_LED.set_color(values)
        led_values[0] = duty_to_rgb(values)
        asyncio.run(ws.send(json.dumps(led_values)))

    def select(pin):
        global box_select
        global selected_line
        global send_data
        
        box_select %= 4
        
        if box_select == 0:
            selected_line = 0
            display.rgb_selection(LABELS, values)
            switch.callback = swap_state
            rotary.callback = select_color
        else:
            led_values[box_select] = not led_values[box_select]
            leds[box_select - 1].value(led_values[box_select])
            
            display.clear()
            display.led_rooms(led_values)
            display.buffer.rect(x_y_pair[box_select][0], x_y_pair[box_select][1], 44, 18, not led_values[box_select], False) # Invert selection box
            display.show()
            asyncio.run(ws.send(json.dumps(led_values)))
    
    switch = DebouncedSwitch(5, select)
    
    def duty_to_rgb(values):
        converted = [0, 0, 0]
        
        for i in range(len(values)):
            converted[i] = round((values[i]/1023)*255)
        
        return converted
    
    while True:
        value = await ws.receive()
        value = json.loads(value)
        try:
            led_values[value['led']] = not led_values[value['led']]
            leds[value['led'] - 1].value(led_values[value['led']])
        except:
            values = hex_to_rgb(value['rgb'])
            RGB_LED.set_color(values)
            display.rgb_display.update_values(values)
        update_display()
        
@app.route('/ldr')
@with_websocket
async def ldr(request, ws):
    LDR = ADC(Pin(36))
    LDR.atten(ADC.ATTN_11DB)
    LDR.width(ADC.WIDTH_10BIT)
    value = LDR.read()
    asyncio.run(ws.send(str(100 - (100 * value / 1028))))
    time.sleep(2)
    ldr(request, ws)

    
def update_display():
    global led_values

    display.clear()
    display.led_rooms(led_values)
    display.show()
    
def box_scroll(value):
    global led_values
    global box_select
    
    box_select += value
    box_select %= 4
    width = 44
    height = 18
    
    display.clear()

    display.led_rooms(led_values)
    if box_select == 0:
        display.buffer.rect(x_y_pair[0][0], x_y_pair[0][1], width, height, True, False)
    else:
        display.buffer.rect(x_y_pair[box_select][0], x_y_pair[box_select][1], width, height, not led_values[box_select], False)
    display.show()

def select_color(value):
    """Shows which color the user is currently "hovering" over"""
    
    global selected_line
    selected_line += value # Value is always either +1 or -1 (CW or CCW)
    display.rgb_display.line_select(selected_line % 4)
    
def hex_to_rgb(hex_val):
    converted = [0, 0, 0]
    hex_val = hex_val[1:] # Chop off the '#' symbol
    
    for i in range(6):
        if not i % 2:
            converted[i//2] = int(hex_val[i:i+2], 16)
            
    return(converted)

rotary = RotaryEncoder(19, 18, box_scroll)

try:
    app.run(port=8080)
finally:
    #RGB_LED.brightness(0)
    display.buffer.fill(0)
    display.show()
