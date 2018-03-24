open_project mmult
set_top mmult
add_files mmult.cpp -cflags -std=c++0x 
add_files -tb main.cpp -cflags -std=c++0x
open_solution "mmult"
set_part {xc7z020clg484-1}
create_clock -period 10 -name default
csim_design -compiler clang
csynth_design
# cosim_design
export_design -format ip_catalog -description "Simple Matrix-Multiply Core for the PYNQ-HLS Tutorial" -vendor "UCSD" -version "1.0" -display_name "Simple Matrix Multiply"
exit
