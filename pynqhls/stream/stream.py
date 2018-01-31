from pynq import Overlay, GPIO, Register
import os
import inspect
class streamOverlay(Overlay):
    """A simple Stream Overlay for PYNQ.

    This overlay is implemented with a single Streaming HLS Core fed by
    a DMA Engine

    """
    __RESET_VALUE = 0
    __NRESET_VALUE = 1
    def __init__(self, bitfile, **kwargs):
        """Initializes a new streamOverlay object.

        """
        # Get file path of the current class (i.e. /opt/python3.6/<...>/stream.py)
        file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
        # Get directory path of the current class (i.e. /opt/python3.6/<...>/stream/)
        dir_path = os.path.dirname(file_path)
        # Update the bitfile path to search in dir_path
        bitfile = os.path.join(dir_path, bitfile)
        super().__init__(bitfile, **kwargs)
        self.__resetPin = GPIO(GPIO.get_gpio_pin(0), "out")
        # self.__AP_CTRL = Register( TODO )
        
    def start(self):
        """ Toggle the startPin GPIO to drive AP_START and enable the HLS
        core"""
        # TODO: Start HLS Core by writing to AP_CTRL
        pass
        
    def reset(self):
        """ Set the reset pin to self.__RESET_VALUE to place the core into
        reset"""
        self.__resetPin.write(self.__RESET_VALUE)

    def run(self, sbuf, dbuf):
        """ Launch computation on the HLS core

        Parameters
        ----------
        sbuf : ContiguousArray
            An xlnk allocated buffer to be transferred to the core
    
        sbuf : ContiguousArray
            An xlnk allocated buffer to be transferred to the core
        """
        self.__resetPin.write(self.__NRESET_VALUE)
        self.start()
        # Load DMA Engine
        # Wait for termination

    def load(self, coeffs):
        """ Load the filter coefficients into the HLS core """
