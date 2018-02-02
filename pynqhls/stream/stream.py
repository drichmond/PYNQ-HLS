from pynq import Overlay, GPIO, Register
from pynq import Xlnk
import numpy as np
import os
import inspect
class streamOverlay(Overlay):
    """A simple Stream Overlay for PYNQ.

    This overlay is implemented with a single Streaming HLS Core fed by
    a DMA Engine

    """
    __RESET_VALUE = 0
    __NRESET_VALUE = 1

    """For convenince, we define a few offsets that are scraped from the
    filt1d implementation header files."""
    __FILT1D_AP_CTRL_OFF = 0x00
    __FILT1D_AP_CTRL_START_IDX = 0
    __FILT1D_AP_CTRL_DONE_IDX  = 1
    __FILT1D_AP_CTRL_IDLE_IDX  = 2
    __FILT1D_AP_CTRL_READY_IDX = 3

    __FILT1D_GIE_OFF     = 0x04
    __FILT1D_IER_OFF     = 0x08
    __FILT1D_ISR_OFF     = 0x0C
    __FILT1D_COEFF_OFFS  = [0x10, 0x18,	0x20, 0x28,
                            0x30, 0x38,	0x40, 0x48,
                            0x50]
    __FILT1D_LENGTH_OFF  = 0x54
    def __init__(self, bitfile, **kwargs):
        """Initializes a new streamOverlay object.

        """
        # The following lines do some path searching to enable a 
        # PYNQ-Like API for Overlays. For example, without these 
        # lines you cannot call streamOverlay('stream.bit') because 
        # stream.bit is not on the bitstream search path. The 
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
        # Define a Register object at address 0x0 of the filt1d address space
        # We will use this to set bits and start the core (see start())
        # Do NOT write to __ap_ctrl unless __resetPin has been set to __NRESET_VALUE
        self.__ap_ctrl = Register(self.filt1d.mmio.base_addr, 32)
        self.xlnk = Xlnk()
        
    def __start(self):
        """Toggle AP_START and enable the HLS core

        """
        self.__ap_ctrl[self.__FILT1D_AP_CTRL_START_IDX] = 0
        self.__ap_ctrl[self.__FILT1D_AP_CTRL_START_IDX] = 1
        self.__ap_ctrl[self.__FILT1D_AP_CTRL_START_IDX] = 0
        pass

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

    def run(self, coeffs, buf):
        """ Launch computation on the HLS core

        Parameters
        ----------
        coeffs: list
            An xlnk allocated buffer to be transferred to the core
    
        buf : list
            An xlnk allocated buffer to be transferred to the core
        """
        self.nreset()
        print("Not in reset!")
        self.__load(coeffs)
        print("Loaded coefficients!")        
        self.filt1d.write(self.__FILT1D_LENGTH_OFF, len(buf))
        print("Wrote Length!") 
        l = len(buf)
        cmabuf_src = self.xlnk.cma_array([l, 1], np.int32)
        for i in range(l):
            cmabuf_src[i] = buf[i]
        print("Allocated Source CMA Array")
        cmabuf_dest = self.xlnk.cma_array([l, 1], np.int32)
        print("Allocated Destination CMA Array")

        self.hlsDmaEngine.recvchannel.transfer(cmabuf_dest)
        print("Started Transmit")        
        self.hlsDmaEngine.sendchannel.transfer(cmabuf_src)
        print("Started Send")
        self.__ap_ctrl[self.__FILT1D_AP_CTRL_START_IDX] = 1

        self.__start()
        print("Pulsed Start!")        

        self.hlsDmaEngine.sendchannel.wait()
        print("Finished Send")
        self.hlsDmaEngine.recvchannel.wait()
        print("Finished recv")        
        self.__ap_ctrl[self.__FILT1D_AP_CTRL_START_IDX] = 0

        buf = cmabuf_dest.tolist()
        cmabuf_dest.freebuffer()
        cmabuf_src.freebuffer()
        return buf

    def __load(self, coeffs):
        """ Load the filter coefficients into the HLS core """
        for (offset, coeff) in zip(self.__FILT1D_COEFF_OFFS, coeffs):
            self.filt1d.write(offset, coeff)
                                   
