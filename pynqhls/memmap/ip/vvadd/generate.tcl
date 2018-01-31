open_project vvadd
set_top vvadd
add_files vvadd.cpp
add_files -tb main.cpp -cflags -std=c++0x
open_solution "vvadd"
set_part {xc7z020clg484-1}
create_clock -period 10 -name default
csim_design
csynth_design
#cosim_design
export_design -format ip_catalog -description "Simple Vector-Vector add core for PYNQ-HLS Tutorial" -vendor "UCSD" -version "1.0" -display_name "Vector-Vector Add"
exit
