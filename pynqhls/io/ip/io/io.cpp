#include "io.hpp"
#include "ap_utils.h"

void check_buttons(const ap_uint<4>& buttons, ap_uint<32>& reg){
	reg = buttons;
}

void count_leds(ap_uint<4>& leds){
	static ap_uint<4> state;
#pragma HLS reset variable=state
	leds = ++state;
}

template <unsigned int MILLISECONDS>
void delay_until_ms(){
#pragma HLS INLINE
#pragma HLS PROTOCOL floating
	volatile char dummy;
	ap_uint<64> ctr;
	ap_uint<64> cyc = (F_OVERLAY_HZ * MILLISECONDS / MSEC_PER_SEC);
	for (ctr = 0; ctr < cyc; ++ctr){
		dummy = dummy;
	}
	return;
}

void io(const ap_uint<32> mem [MEM_SPACE_SIZE],
	ap_uint<32> reg[REG_SPACE_SIZE],
	const ap_uint<4> buttons,
	ap_uint<4>& leds){
/* Define a new AXI-Lite bus named CTRL for HLS Status/Control registers
   (return), and for the register space*/
#pragma HLS INTERFACE m_axi port=mem offset=slave bundle=MEM
#pragma HLS INTERFACE s_axilite port=return bundle=CTRL
#pragma HLS INTERFACE s_axilite port=reg    bundle=CTRL
#pragma HLS INTERFACE ap_none port=leds


	check_buttons(buttons, reg[1]);
	count_leds(leds);
	delay_until_ms<1000>();	
	return;
}
