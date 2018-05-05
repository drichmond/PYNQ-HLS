# PYNQ-HLS Tutorial

This repository is a tutorial for using High-Level Synthesis cores in
PYNQ. It can be used as a three-part lab curriculum, or as a
standalone tutorial for PYNQ.

To install this repository, simply run the following commands on your PYNQ board: 

``` bash
git clone https://github.com/drichmond/PYNQ-HLS ~/PYNQ-HLS
sudo -H pip3.6 install ~/PYNQ-HLS
```

This will clone and install the tutorials to your PYNQ board. 


This repository has three topics: 

1. Streaming HLS Cores
2. Shared-Memory HLS Cores
3. Real-Time IO HLS Cores


## Streaming HLS Cores
This tutorial teaches a reader how to use an HLS core with
AXI-Streaming interfaces in PYNQ. The completed demonstration
notebook for this tutorial can be found in `<Jupyter
Home>/HLS-Demo/streaming`. The tutorial notebooks can be found
inside the `<Jupyter Home>/HLS-Tutorial/streaming`
	
This topic is useful for image and signal processing applications.
	
## Shared-Memory HLS Cores
This tutorial teaches a reader how to use an HLS core that interacts
with memory shared between the ARM PS and FPGA PL. The completed
demonstration notebook for this tutorial can be found in `<Jupyter
Home>/HLS-Demo/streaming`. The tutorial notebooks can be found
inside the `<Jupyter Home>/HLS-Tutorial/streaming`

This topic is useful for bulk data processing applications, such as
matrix multiply.

## Real-Time IO HLS Cores
This tutorial teaches a reader how to implement and use a Real-Time
HLS core. The completed demonstration notebook for this tutorial can
be found in `<Jupyter Home>/HLS-Demo/streaming`. The tutorial
notebooks can be found inside the `<Jupyter
Home>/HLS-Tutorial/streaming`

This topic is useful for general GPIO, and real-time motor
controllers.


Feedback, pull requests, and suggestions greatly appreciated
