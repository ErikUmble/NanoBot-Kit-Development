import time
from machine import Pin
import ubluetooth

led = Pin(6, Pin.OUT)

bt = ubluetooth.BLE()
bt.active(True)
bt.config(ble_name='NanoBot')

def conn_cb(bt_o):
    events = bt_o.events()
    if  events & bt_o.CLIENT_CONNECTED:
        print("Client connected")

bt.callback(trigger=bt.CLIENT_CONNECTED | bt.CLIENT_DISCONNECTED, handler=conn_cb)
bt.start_advertising()

# Define the UUIDs for your custom service and characteristic
SERVICE_UUID = ubluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
CHARACTERISTIC_UUID = ubluetooth.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E')

# Create the service and characteristic
uart = bt.service(uuid=SERVICE_UUID, isprimary=True)
tx = uart.characteristic(uuid=CHARACTERISTIC_UUID, properties=ubluetooth.BLE.WRITE | ubluetooth.BLE.NOTIFY)

# Set advertising data
bt.gap_advertise(100, adv_data)

# Function to handle write events on the characteristic
def char_write_callback(char):
    value = char.value()
    print("Received data:", value)

# Set the write callback for the characteristic
tx.callback(trigger=tx.WRITE, handler=char_write_callback)

while (True):


    # Process BLE events
    bt.gap_scan(1000)  # Adjust the timeout value as needed
    # Discover services and characteristics
    services = bt.get_services()
    for service in services:
        print("Service UUID:", service.uuid())
        for char in service.characteristic():
            print("Characteristic UUID:", char.uuid())
            '''for char in service.characteristic():
                    if char.uuid() == target_uuid:
                        value = char.read()
                        print("Characteristic Value:", value)'''
