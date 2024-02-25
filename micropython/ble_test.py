import bluetooth
import time
from micropython import const
from ble_advertising import advertising_payload

_IO_CAPABILITY_DISPLAY_ONLY = const(0)

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_IRQ_GATTC_INDICATE = const(19)

_FLAG_READ = const(0x0002)
_FLAG_WRITE = const(0x0008)

_SERVICE_UUID = bluetooth.UUID(0x1523)
_LED_CHAR_UUID = (bluetooth.UUID(0x1525), _FLAG_WRITE | _FLAG_READ)
_LED_SERVICE = (_SERVICE_UUID, (_LED_CHAR_UUID,),)

class BLETemperature:
    def __init__(self, ble, name="NANO RP2040"):
        self._ble = ble
        self._ble.active(True)
        self._ble.config(
            bond=True,
            mitm=True,
            le_secure=True,
            io=_IO_CAPABILITY_DISPLAY_ONLY
        )
        self._ble.irq(self._irq)
        ((self._handle,),) = self._ble.gatts_register_services((_LED_SERVICE,))
        self._connections = set()
        self._payload = advertising_payload(name=name, services=[_SERVICE_UUID])
        self._advertise()

    def _irq(self, event, data):
        print("Event:", event, "data:", data)
        if event == _IRQ_CENTRAL_CONNECT:
            # Mobile has (already?) been successful in attempting to connected
            conn_handle, addr_type, addr = data
            self._connections.add(conn_handle)
            print("1:", conn_handle, addr_type, addr)

        elif event == _IRQ_CENTRAL_DISCONNECT:
            # Mobile has disconnected
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            self._advertise()

        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            if conn_handle in self._connections:
                # Value has been written to the LED characteristic
                value = self._ble.gatts_read(value_handle)
                print("Value written to LED characteristic:", value)

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

if __name__ == "__main__":
    ble = bluetooth.BLE()
    temp = BLETemperature(ble)

    while True:
        time.sleep_ms(1000)
