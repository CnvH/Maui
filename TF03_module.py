'''Class declarations for Benewake TF03 LiDar'''
from machine import UART


class TF_03:
    def __init__(self):
        self.msg_max_size = 10 #todo edit init so that msg_max_size and uart info is passed to TF03
        self.buf = bytearray(self.msg_max_size)
        self.uart = UART(2,115200)
        self.uart.init(115200, bits=8, parity=None, stop=1)
    def load_buf(self):
