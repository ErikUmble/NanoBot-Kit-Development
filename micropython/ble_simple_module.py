import bluetooth
import time
from micropython import const
from ble_advertising import advertising_payload

# Define constants (these are not packaged in bluetooth for space efficiency)
_IO_CAPABILITY_DISPLAY_ONLY = const(0)
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
_IRQ_GATTC_INDICATE = const(19)
_FLAG_READ = const(0x0002)
_FLAG_WRITE = const(0x0008)

# Setup bluetooth low energy communication service
_SERVICE_UUID = bluetooth.UUID(0x1523) # unique service id for the communication
_NanoBot_CHAR_UUID = (bluetooth.UUID(0x1525), _FLAG_WRITE | _FLAG_READ) # characteristic
_NanoBot_SERVICE = (_SERVICE_UUID, (_NanoBot_CHAR_UUID,),) # service to provide the characteristic

class NanoBotBLE:
    def __init__(self, ble, name="NANO RP2040"):
        self._ble = ble
        self._ble.active(True)
        self._ble.config(
            bond=True,
            mitm=True,
            le_secure=True,
            io=_IO_CAPABILITY_DISPLAY_ONLY
        )
        #self._ble.irq(self._irq)  # optional event handler
        ((self._handle,),) = self._ble.gatts_register_services((_NanoBot_SERVICE,))
        self._connections = set()
        self._payload = advertising_payload(name=name, services=[_SERVICE_UUID])
        self._advertise()

    def _irq(self, event, data):
        # no need to handle bluetooth events for this application
        pass
        # handle bluetooth event
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

    def send(self, value):
        # Writes value (as byte) to characteristic

        # Convert value to bytes if it's not already
        if not isinstance(value, bytes):
            if isinstance(value, int):
                value = value.to_bytes(1, "big")
            elif isinstance(value, str):
                value = value.encode('utf-8')
            else:
                raise ValueError("send value should be type bytes, int, or string")
        self._ble.gatts_write(self._handle, value)

    def read(self, as_type="bytes"):
        value = self._ble.gatts_read(self._handle)
        if as_type == "bytes":
            return value
        elif as_type == "str":
            return value.decode("utf-8")
        elif as_type == "int":
            return int.from_bytes(value, "big")

        raise ValueError("as_type must be one of 'bytes', 'str', or 'int'")

if __name__ == "__main__":
    ble = bluetooth.BLE()
    nanobot_ble = NanoBotBLE(ble)

    while True:
        time.sleep_ms(5000)
        print(nanobot_ble.read("int"))
        nanobot_ble.send(0x51)
