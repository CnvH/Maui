
from TF03_module import TF03
from machine import sleep



x = TF03()

print('Hello From ESP32')

cmd_ver = bytearray(4)
cmd_ver[0] = 0x59
cmd_ver[1] = 0x04
cmd_ver[2] = 0x01
cmd_ver[3] = 0x5E

range_old = 0
i = 1

x.uart.write(0x59)
x.uart.write(0x04)
x.uart.write(0x01)
x.uart.write(0x5E)

while i <= 50:
  if x.load_buf():
    range = x.range(False)
    sleep(100)

    print('Range: ' ,range ,'cm')
    range_old = range
    i += 1
