open_project filt1d
set_top filt1d
add_files filt1d.cpp
add_files -tb main.cpp -cflags -std=c++0x
open_solution "filt1d"
set_part {xc7z020clg484-1}
create_clock -period 10 -name default
csim_design
csynth_design
# cosim_design
export_design -format ip_catalog -description "Simple 1-D Filter for PYNQ-HLS Tutorial" -vendor "UCSD" -version "1.0" -display_name "Simple 1-D Filter"
exit
