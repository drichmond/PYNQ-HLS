from pynq import Overlay, GPIO, Register, Xlnk
import os
import inspect
import numpy as np
class sharedmemOverlay(Overlay):
    """A simple Mem-Mapped Overlay for PYNQ.

    This overlay is implemented with a single Matrix Multiply Core fed
    connected directly to the ARM Core AXI interface.

    """
    __RESET_VALUE = 0
    __NRESET_VALUE = 1

    """ For convenince, we define register offsets that are scraped from
    the HLS implementation header files.

    """
    __MMULT_AP_CTRL_OFF = 0x00
    __MMULT_AP_CTRL_START_IDX = 0
    __MMULT_AP_CTRL_DONE_IDX  = 1
    __MMULT_AP_CTRL_IDLE_IDX  = 2
    __MMULT_AP_CTRL_READY_IDX = 3

    __MMULT_GIE_OFF     = 0x04
    __MMULT_IER_OFF     = 0x08
    __MMULT_ISR_OFF     = 0x0C

    __MMULT_ADDR_A_DATA = 0x10
    __MMULT_ADDR_BT_DATA = 0x18
    __MMULT_ADDR_C_DATA = 0x20

    __MMULT_A_SHAPE = (100, 100)
    __MMULT_BT_SHAPE = (100, 100)
    __MMULT_C_SHAPE = (100, 100)
    __MMULT_A_SIZE = __MMULT_A_SHAPE[0] * __MMULT_A_SHAPE[1]
    __MMULT_BT_SIZE = __MMULT_BT_SHAPE[0] * __MMULT_BT_SHAPE[1]
    __MMULT_C_SIZE = __MMULT_C_SHAPE[0] * __MMULT_C_SHAPE[1]
    

    def __init__(self, bitfile, **kwargs):
        """Initializes a new sharedmemOverlay object.

        """
        # The following lines do some path searching to enable a 
        # PYNQ-Like API for Overlays. For example, without these 
        # lines you cannot call sharedmemOverlay('sharedmem.bit') because 
        # sharedmem.bit is not on the bitstream search path. The 
        # following lines fix this for any non-PYNQ Overlay
        #
        # You can safely reuse, and ignore the following lines
        #
        # Get file path of the current class (i.e. /opt/python3.6/<...>/sharedmem.py)
        file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
        # Get directory path of the current class (i.e. /opt/python3.6/<...>/sharedmem/)
        dir_path = os.path.dirname(file_path)
        # Update the bitfile path to search in dir_path
        bitfile = os.path.join(dir_path, bitfile)
        # Upload the bitfile (and parse the colocated .tcl script)
        super().__init__(bitfile, **kwargs)
        # Manually define the GPIO pin that drives reset
        self.__resetPin = GPIO(GPIO.get_gpio_pin(0), "out")
        self.nreset()
        # Define a Register object at address 0x0 of the mmult address space
        # We will use this to set bits and start the core (see start())
        # Do NOT write to __ap_ctrl unless __resetPin has been set to __NRESET_VALUE
        self.__ap_ctrl = Register(self.mmultCore.mmio.base_addr, 32)
        self.__a_offset = Register(self.mmultCore.mmio.base_addr +
                                       self.__MMULT_ADDR_A_DATA, 32)
        self.__bt_offset = Register(self.mmultCore.mmio.base_addr +
                                       self.__MMULT_ADDR_BT_DATA, 32)
        self.__c_offset = Register(self.mmultCore.mmio.base_addr +
                                       self.__MMULT_ADDR_C_DATA, 32)
        self.xlnk = Xlnk()

    def __start(self):
        """Raise AP_START and enable the HLS core

        """
        self.__ap_ctrl[self.__MMULT_AP_CTRL_START_IDX] = 1
        pass

    def __stop(self):
        """Lower AP_START and disable the HLS core

        """
        self.__ap_ctrl[self.__MMULT_AP_CTRL_START_IDX] = 0
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

    def run(self, A, B):
        """ Launch computation on the mmult HLS core

        Parameters
        ----------
    
        A : Numpy ndarray of at most size TODOxTODO (it will be padded)
            A buffer containing ND Array Elements to be transferred to the core

        B : Numpy ndarray of at most size TODOxTODO (it will be padded)
            A buffer containing ND Array Elements to be transferred to the core

        """
        if(not isinstance(A, np.ndarray)):
            raise TypeError("Parameter A must be an instance of "
                                   "numpy.ndarray")

        if(not isinstance(B, np.ndarray)):
            raise RuntimeError("Parameter B must be an instance of "
                                   "numpy.ndarray")
        sza = A.shape
        if(sza[0] > self.__MMULT_A_SHAPE[0]):
            raise RuntimeError(f"Dimension 0 of A must be less than or equal to"
                                   f"{self.__MMULT_A_SHAPE[0]}")
        if(sza[1] > self.__MMULT_A_SHAPE[1]):
            raise RuntimeError(f"Dimension 1 of A must be less than or equal to"
                                   f"{self.__MMULT_A_SHAPE[1]}")

        szb = B.shape
        if(szb[0] > self.__MMULT_BT_SHAPE[1]):
            raise RuntimeError(f"Dimension 0 of B must be less than or equal to"
                                   f"{self.__MMULT_BT_SHAPE[0]}")
        if(szb[1] > self.__MMULT_BT_SHAPE[0]):
            raise RuntimeError(f"Dimension 1 of B must be less than or equal to"
                                   f"{self.__MMULT_BT_SHAPE[1]}")


        # Check size of A
        # Check size of B
        # Allocate C
        a = self.xlnk.cma_array(self.__MMULT_A_SHAPE, "int")
        bt = self.xlnk.cma_array(self.__MMULT_BT_SHAPE, "int")
        c = self.xlnk.cma_array(self.__MMULT_C_SHAPE, "int")
        # Copy A->a
        a[:A.shape[0], :A.shape[1]] = A
        # Copy BT->bt
        bt[:B.shape[1], :B.shape[0]] = B.transpose()
        # TODO: Enable Interrupts
        # Write address of a, bt, c to HLS core
        self.__a_offset[31:0]  = self.xlnk.cma_get_phy_addr(a.pointer)
        self.__bt_offset[31:0] = self.xlnk.cma_get_phy_addr(bt.pointer)
        self.__c_offset[31:0]  = self.xlnk.cma_get_phy_addr(c.pointer)
        self.__start()
        # TODO: Wait for ASYNC Interrupt
        # TODO: Clear Interrupt
        import time
        time.sleep(1)
        self.__stop()
        C = np.zeros((A.shape[0], B.shape[1]), np.int32)
        # Transform C into a Numpy Array
        C[:A.shape[0], :B.shape[1]] = c[:A.shape[0], :B.shape[1]]
        a.freebuffer()
        bt.freebuffer()
        c.freebuffer()
        return C
