# RISC-V

This folder contains the bare-bones files that are used in the How-To-RISC-V
tutorial. You can install the tutorial on your PYNQ board by following the
instructions in the parent directory.

It contains the following files and folders:

- README.md: This file.

- vivado: A folder containing the Vivado source and constraint files for
  implementing the tutorial on the PYNQ-Z1 board.

- ip: A folder containing a custom interface definition for PCPI and destination
  for the picorv32 IP block created during the tutorial.

- riscv.tcl: A bare-bones tcl script used and modified in the tutorial. The
  script creates a Vivado 2017.1 project titled **riscv** and instantiates a
  Zynq 7000 PS with the correct settings for the PYNQ-Z1 board.

- makefile: A makefile for Unix-like interfaces that will run the riscv.tcl file
  without opening the Vivado GUI.

During the tutorial you will create the following files in this folder:

- ip/picorv32: A Vivado IP block encapuslating the picorv32 RISC-V processor.

- notebooks: A placeholder for notebooks. This file will contain a RISC-V
  makefile, Hex-Converter script, and a Linker script. It will be moved onto
  your PYNQ board.

- riscv.bit: A FPGA bit file with the picorv32 RISC-V processor instantiated and
  connected.


