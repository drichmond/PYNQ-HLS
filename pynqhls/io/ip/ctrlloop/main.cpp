#include "ctrlloop.hpp"
#include <random>
#include <stdio.h>

int main(){
	ap_uint<32> mem [IOMEM_SPACE_SIZE];
	ap_uint<32> reg [REG_SPACE_SIZE];
	ap_uint<4> buttons = 0xA;
	ap_uint<4> leds = 0;

	ctrlloop(mem, reg, buttons, leds);
	
	if(reg[0] != buttons){
		printf("Fail! Value of buttons not written to reg array!\n");
		return -1;
	}
		
	if(leds != 1){
		printf("Fail! Value of leds was not 1!\n");
		return -1;
	}

	return 0;
}
