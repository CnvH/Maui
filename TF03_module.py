'''Class declarations for Benewake TF03 LiDar'''
from machine import UART


class TF_03:

    def __init__(self):
        self.msg_max_size = 10
        self.buf = bytearray(self.msg_max_size)
        self.uart = UART(2,115200)
        self.uart.init(115200, bits=8, parity=None, stop=1)
        self.ptr=-1  #if ptr>-1 then the buf is part full with an incomplete message
        self.frame_marker = 0x50  # this is the magic character that marks the start of a TF03 data frame
    def load_buf(self):
        num_to_read = self.uart.any()

        while (num_to_read > self.ptr):
            ch = self.uart.read(1)
            if (self.ptr == -1) & (ch == self.frame_marker):  #Found the start of a new data frame from the TF03
                self.buf[0] = ch
                self.ptr = 0
            elif self.ptr == 0  #we are at the second value in the data fram
                self.buf[1] = ch
                self.ptr = 1
                if ch == self.frame_marker:  #this is the special case of a lidar range frame of 9 bytes (7 left)
                    num_to_read = 7
