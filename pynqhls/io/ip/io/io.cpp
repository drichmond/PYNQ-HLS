#include "io.hpp"
#include "ap_utils.h"

void check_buttons(const ap_uint<4>& buttons, ap_uint<32>& reg){
	reg = buttons;
}

void count_leds(ap_uint<4>& leds){
	static ap_uint<4> state;
	leds = ++state;
}
#define MSEC_PER_SEC (1000)
template <unsigned int MSEC>
void delay_until_ms(){
	const unsigned int ctr = (F_OVERLAY_HZ*MSEC / (MSEC_PER_SEC));
	for (unsigned int i = 1; i < ctr; ++i){
#pragma HLS PIPELINE
		ap_wait();
	}
}

void io(const ap_uint<32> mem [MEM_SPACE_SIZE],
	ap_uint<32> reg[REG_SPACE_SIZE],
	const ap_uint<4> buttons,
	ap_uint<4>& leds){
/* Define a new AXI-Lite bus named CTRL for HLS Status/Control registers
   (return), and for the register space*/
#pragma HLS INTERFACE m_axi port=mem offset=slave bundle=MEM
#pragma HLS INTERFACE s_axilite port=return bundle=CTRL
#pragma HLS INTERFACE s_axilite port=reg    bundle=CTRL offset = 0x1
#pragma HLS INTERFACE ap_none port=leds
#pragma HLS DATAFLOW
	check_buttons(buttons, reg[1]);
	count_leds(leds);
	delay_until_ms<MSEC_PER_SEC>();
}
