
"""Class declarations for Benewake TF03 LiDar"""
from machine import UART


class TF03:
    def range(self, show = True):
        range_cm = self.buf[3]*256+self.buf[2]
        if show:
          print('Range : ',range_cm,'cm')
        return range_cm

    def __init__(self):
        def no_handler(calling_msg):
            print('no handler for message: ',calling_msg)


        self.msg_max_size = 10
        self.buf = bytearray(self.msg_max_size)
        self.uart = UART(2, 115200)
        self.uart.init(115200, bits=8, parity=None, stop=1)
        self.ptr = -1  # if ptr>-1 then the buf is part full with an incomplete message
        self.frame_marker = 0x59  # this is the magic character that marks the start of a TF03 data frame
        self.comms_errors = 0
        self.num_to_read = 0
        self.frame_size = 999
        self.handlers = {
            # todo setup with format is msg number (byte 3 of message), Command Function, Response Function
            0x59: range,
            0x01: no_handler,
            0x02: no_handler,
            0x03: no_handler,
            0x04: no_handler,
            0x05: no_handler,
            0x06: no_handler,
            0x08: no_handler,
            0x10: no_handler,
            0x11: no_handler,
            0x45: no_handler,
            0x4F: no_handler,
            0x50: no_handler,
            0x51: no_handler,
            0x52: no_handler,
            0x5D: no_handler,
            0x61: no_handler,
            0x62: no_handler,
            0x63: no_handler,
            0x64: no_handler,
            0x69: no_handler,
        }
    # ====== end of __init()__ ======

    def load_handler_func(self,trigger,handler_func):
        if self.handlers.get(trigger, lambda: False):
            self.handlers[trigger] = handler_func
        else:
            print("load_handler called to assign handler to unknown trigger: ", trigger)

    # ====== end of load_handler_func() ======

    def load_buf(self):
        num_available = self.uart.any() # number of bytes available to read from uart
        if num_available == 0:  # nothing to read...
            # print('xxxxx UART Empty xxxxx')
            return False

        # print('num_available: ',num_available)

        if self.num_to_read == 0:
            self.num_to_read = num_available

        while self.num_to_read > 0:
            ch = self.uart.read(1)[0]
            self.num_to_read -= 1 # 1 byte read from uart
            # print('num_to_read: ',self.num_to_read,'   ch: ',ch)

            if (self.ptr == -1) & (ch == self.frame_marker):  # Found the start of a new data frame from the TF03
                self.buf[0] = ch
                self.ptr = 0
            elif self.ptr == 0:  # we are at the second value in the data frame
                self.buf[1] = ch
                self.ptr = 1
                if ch == self.frame_marker:
                    self.frame_size = 9 # this is the special case of a lidar range frame of 9 bytes
                else:
                    self.frame_size = ch  # otherwise frame size is in the second byte (ptr == 1)
                self.num_to_read = min(self.frame_size-2,self.num_to_read)
            elif self.ptr >= 1:
                self.ptr += 1
                self.buf[self.ptr] = ch

            #print('num_available: ',num_available,'  num_to_read: ',self.num_to_read,'  ch: ',ch,'  ptr: ',self.ptr)

        # this point is reached if 1) there is nothing left to read without a frame being detected,
        # 2) a frame has been partly collected, or 3) a complete frame has been collected
        if (self.frame_size - 1) == self.ptr:   # this means a complete frame has been read
            # checksum check goes here
            self.ptr = -1
            self.num_to_read = 0
            # check size of frame and checksum.  If not good self.comms_errors++ and return false
            return True
        else:
            # either ptr still is -1 because nothing has been read or ptr is a value from which reading can continue
            return False

        # todo need to track this through execution and notify when buf is complete after checksum check
    # ====== end of load_buf() ======
    def write_TF03(self,command):
        # command is a bytearray
        pass