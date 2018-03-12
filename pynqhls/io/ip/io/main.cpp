#include "io.hpp"
#include <random>
#include <stdio.h>

int main(){
	ap_uint<32> mem [MEM_SPACE_SIZE];
	ap_uint<32> reg[REG_SPACE_SIZE];
	ap_uint<4> buttons;
	ap_uint<4> leds;

	io(mem, reg, buttons, leds);

	return 0;
}
