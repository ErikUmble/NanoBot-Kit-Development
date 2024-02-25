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
_FLAG_NOTIFY = const(0x0010)
_FLAG_INDICATE = const(0x0020)
_FLAG_WRITE = const(0x0008)

_SERVICE_UUID = bluetooth.UUID(0x1523)
_MyTest_CHAR_UUID = (bluetooth.UUID(0x1525), _FLAG_READ | _FLAG_NOTIFY | _FLAG_INDICATE | _FLAG_WRITE)
_MyTest_SERVICE = (_SERVICE_UUID, (_MyTest_CHAR_UUID,),)

class BLETest:
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
        ((self._handle,),) = self._ble.gatts_register_services((_MyTest_SERVICE,))
        self._connections = set()
        self._payload = advertising_payload(name=name, services=[_SERVICE_UUID])
        self._advertise()

    def _irq(self, event, data):
        if event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            if conn_handle in self._connections:
                # Value has been written to the LED characteristic
                value = self._ble.gatts_read(value_handle)
                print("Value written to LED characteristic:", value)

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

if __name__ == "__main__":
    ble = bluetooth.BLE()
    temp = BLETest(ble)

    while True:
        time.sleep_ms(1000)
