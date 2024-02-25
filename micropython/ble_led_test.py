# More details can be found in TechToTinker.blogspot.com
# George Bantique | tech.to.tinker@gmail.com
from machine import Pin
from machine import UART
from machine import Timer
from time import ticks_ms

bt = UART(2, baudrate=9600, tx=25, rx=23)
led = Pin(6, Pin.OUT)
sw = Pin(0, Pin.IN)

tim0 = Timer(0)
t_start = ticks_ms()

while True:
    if bt.any()!=0:
        msg = bt.read(bt.any()).decode().strip('rn')
        print(msg)
        msg = bt.read(bt.any()).decode()
        if "ON" in msg:
            led.value(1)
            tim0.deinit()
            print('LED is ON')
        elif "OFF" in msg:
            led.value(0)
            tim0.deinit()
            print('LED is OFF')
        elif "BLINK" in msg:
            tim0.init(period=250, mode=Timer.PERIODIC, callback=lambda t: led.value(not led.value()))
            print('LED is blinking')
        else:
            print(msg.strip('rn'))
            if ticks_ms()-t_start >= 300:
                if sw.value()==0: # BOOT button is pressed
                    bt.write('Boot button is pressed.rn')
                    print('Sending "Boot button is pressed."')
                    t_start=ticks_ms()
