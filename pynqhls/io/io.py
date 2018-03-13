from pynq import Overlay, GPIO, Register, MMIO
import os
import inspect
import numpy as np
class ioOverlay(Overlay):
    """A simple Mem-Mapped Overlay for PYNQ.

    This overlay is implemented with a single Matrix Multiply Core fed
    connected directly to the ARM Core AXI interface.

    """
    __RESET_VALUE = 0
    __NRESET_VALUE = 1

    """ For convenince, we define register offsets that are scraped from
    the HLS implementation header files.

    """
    __IO_AP_CTRL_OFF = 0x00
    __IO_AP_CTRL_START_IDX = 0
    __IO_AP_CTRL_DONE_IDX  = 1
    __IO_AP_CTRL_IDLE_IDX  = 2
    __IO_AP_CTRL_READY_IDX = 3
    __IO_AP_CTRL_AUTORESTART_IDX = 7

    __IO_GIE_OFF     = 0x04
    __IO_IER_OFF     = 0x08
    __IO_ISR_OFF     = 0x0C
    
    """These define the 'reg' argument to the 'io' HLS function.  The
    memory space defined here is shared between the HLS core and the
    ARM PS.

    """
    __IO_REG_OFF = 0x200
    __IO_REG_LEN = 0x100
    def __init__(self, bitfile, **kwargs):
        """Initializes a new ioOverlay object.

        """
        # The following lines do some path searching to enable a 
        # PYNQ-Like API for Overlays. For example, without these 
        # lines you cannot call ioOverlay('io.bit') because 
        # io.bit is not on the bitstream search path. The 
        # following lines fix this for any non-PYNQ Overlay
        #
        # You can safely reuse, and ignore the following lines
        #
        # Get file path of the current class (i.e. /opt/python3.6/<...>/stream.py)
        file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
        # Get directory path of the current class (i.e. /opt/python3.6/<...>/stream/)
        dir_path = os.path.dirname(file_path)
        # Update the bitfile path to search in dir_path
        bitfile = os.path.join(dir_path, bitfile)
        # Upload the bitfile (and parse the colocated .tcl script)
        super().__init__(bitfile, **kwargs)
        # Manually define the GPIO pin that drives reset
        self.__resetPin = GPIO(GPIO.get_gpio_pin(0), "out")
        # Define a Register object at address 0x0 of the IO address space
        # We will use this to set bits and start the core (see start())
        # Do NOT write to __ap_ctrl unless __resetPin has been set to __NRESET_VALUE
        self.nreset()
        self.__ap_ctrl = Register(self.ioCore.mmio.base_addr, 32)
        self.__hls_reg = MMIO(self.ioCore.mmio.base_addr + self.__IO_REG_OFF,
                              self.__IO_REG_LEN)

    def __set_autorestart(self):
        """ Set the autorestart bit of the HLS core
        """
        self.__ap_ctrl[self.__IO_AP_CTRL_AUTORESTART_IDX] = 1

    def __clear_autorestart(self):
        """ Clear the autorestart bit
        """
        self.__ap_ctrl[self.__IO_AP_CTRL_AUTORESTART_IDX] = 0

    def __start(self):
        """Raise AP_START and enable the HLS core

        """
        self.__ap_ctrl[self.__IO_AP_CTRL_START_IDX] = 1

    def __stop(self):
        """Lower AP_START and disable the HLS core

        """
        self.__ap_ctrl[self.__IO_AP_CTRL_START_IDX] = 0

    def nreset(self):
        """Set the reset pin to self.__NRESET_VALUE to place the core into
        not-reset (usually run)

        """
        self.__resetPin.write(self.__NRESET_VALUE)
        
    def reset(self):
        """Set the reset pin to self.__RESET_VALUE to place the core into
        reset

        """
        self.__resetPin.write(self.__RESET_VALUE)

    def launch(self):
        self.__set_autorestart()
        self.__start()
        
    def land(self):
        self.__clear_autorestart()
        while(not self.__ap_ctrl[self.__IO_AP_CTRL_DONE_IDX]):
            pass
        self.__stop()

    def run(self):
        """ Launch computation on the io HLS core
        
        Returns
        -------
        The 4-bit value representing the value of the buttons.
        
        """
        self.__start()
        while(not self.__ap_ctrl[self.__IO_AP_CTRL_DONE_IDX]):
            pass
        return self.__hls_reg.read(4)
