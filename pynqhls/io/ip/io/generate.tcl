open_project io
set_top io
add_files io.cpp -cflags -std=c++0x 
add_files -tb main.cpp -cflags -std=c++0x
open_solution "io"
set_part {xc7z020clg484-1}
create_clock -period 10 -name default
#csim_design -compiler clang
csynth_design
# cosim_design
export_design -format ip_catalog -description "Simple IO core for the PYNQ-HLS Tutorial" -vendor "UCSD" -version "1.0" -display_name "Simple IO Core"
exit
