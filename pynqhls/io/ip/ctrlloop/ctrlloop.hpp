#ifndef __CTRLLOOP_HPP
#define __CTRLLOOP_HPP

#include "ap_int.h"

#define IOMEM_SPACE_SIZE 4096
#define REG_SPACE_SIZE 128


/* delay_until_ms - Delay for a set number of milliseconds. The length of the
   delay is equal to the frequency of the overlay (F_OVERLAY_HZ) times the
   duration in milliseconds (MILLISECONDS), divided by the number of
   milliseconds in a second (MSEC_PER_SEC)
 */
template <unsigned long long MILLISECONDS, unsigned long long F_OVERLAY_HZ = 50000000ULL>
void delay_until_ms(){
#define MSEC_PER_SEC 1000
#pragma HLS INLINE
#pragma HLS PROTOCOL floating
	volatile char dummy;
	unsigned long long ctr;
	unsigned long long cyc = (F_OVERLAY_HZ * MILLISECONDS / MSEC_PER_SEC);
	for (ctr = 0; ctr < cyc; ++ctr){
		dummy = dummy;
	}
	return;
#undef MSEC_PER_SEC
}

/* ctrlloop - A control loop function. Using the AP_AUTORESTART bit of the
 * AP_CTRL register this loop implements a real-time control loop.
 *
 * mem - ap_uint<32> - An array representing the peripheral memory space. This
 * will become an AXI-Master bus through the use of pragmas
 *
 * regs - ap_uint<32> - An array representing the internal memory space
 * (registers) of the core. The function can read and write to locations
 * here. This will be accessible from the ARM core using the CTRL AXI-Slave bus
 *
 * buttons - const ap_uint<4> - An ap_uint representing the current value on the
 * 4 buttons switches on the PYNQ board. The const specifier will make this
 * default to a 4-bit input port on the HLS core
 * 
 * leds - ap_uint<4>& - An ap_uint for assigning values to the LEDs. Using
 * pragmas this will become a 4-bit output port
 */
void ctrlloop(ap_uint<32> iomem [IOMEM_SPACE_SIZE],
	ap_uint<32> regs[REG_SPACE_SIZE],
	const ap_uint<4> buttons,
	ap_uint<4>& leds);
#endif
