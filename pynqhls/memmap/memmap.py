from pynq import Overlay, GPIO, Register
import os
import inspect
class memmapOverlay(Overlay):
    """A simple Mem-Mapped Overlay for PYNQ.

    This overlay is implemented with a single Mem-Mapped HLS Core fed by
    a DMA engine

    """
    __RESET_VALUE = 0
    __NRESET_VALUE = 1
    def __init__(self, bitfile, **kwargs):
        """Initializes a new memmapOverlay object.

        """
        # Get file path of the current class (i.e. /opt/python3.6/<...>/stream.py)
        file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
        # Get directory path of the current class (i.e. /opt/python3.6/<...>/stream/)
        dir_path = os.path.dirname(file_path)
        # Update the bitfile path to search in dir_path
        bitfile = os.path.join(dir_path, bitfile)
        super().__init__(bitfile, **kwargs)
        self.__resetPin = GPIO(GPIO.get_gpio_pin(0), "out")
        # TODO: Start HLS Core by writing to AP_CTRL
        # self.__AP_CTRL = Register( TODO )
    def start(self):
        """ Toggle the startPin GPIO to drive AP_START and enable the HLS
        core"""
        # TODO
        pass
        
    def reset(self):
        """ Set the reset pin to self.__RESET_VALUE to place the core into
        reset"""
        self.__resetPin.write(self.__RESET_VALUE)

    def run(self, buf):
        """ Launch computation on the HLS core

        Parameters
        ----------
        buf : ContiguousArray
            An xlnk allocated buffer to be transferred to the core
    
        """
        self.__resetPin.write(self.__NRESET_VALUE)
        self.start()
        # Load DMA Engine
        # Wait for termination
