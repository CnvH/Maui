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
                else:
                    num_to_read = ch  # todo this needs a range check in case of corruption
            else:
                self.buf[self.ptr] = ch
                self.ptr += 1

        #this point is reached if there is nothing left to read without a frame being detected,
        # a frame has been collected, or a frame is partly collected
        if num_to_read == ptr: #this means a complete frame has been read
            #checksum check goes here
            self.ptr = -1
            return True
        else:
            #either ptr still is -1 because nothing has been read or ptr is a value from which reading can continue
            return False

        #todo need to track this through execution and notify when buf is complete after checksum check
