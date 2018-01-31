#include "filt1d.hpp"

void filt1d(int *INPUT, int *OUTPUT,
		int coeff[C_NUM_COEFF], unsigned int length){
#pragma HLS INTERFACE axis depth=50 port=INPUT
#pragma HLS INTERFACE axis depth=50 port=OUTPUT
#pragma HLS INTERFACE s_axilite port=coeff  bundle=CTRL
#pragma HLS INTERFACE s_axilite port=length bundle=CTRL
#pragma HLS INTERFACE s_axilite port=return bundle=CTRL
#pragma HLS ARRAY_PARTITION COMPLETE variable=coeff

	int window[C_NUM_COEFF] = {0};
	int sum;

	for (unsigned int i = 0 ; i < length; i++) {
#pragma HLS PIPELINE
		for (unsigned int wi = C_NUM_COEFF-1; wi > 0; --wi){
#pragma HLS UNROLL
			window[wi] = window[wi - 1];
		}
		window[0] = *INPUT++;
		sum = 0;
		for (unsigned int wi = 0; wi < C_NUM_COEFF; ++wi){
#pragma HLS UNROLL
			sum += coeff[wi] * window[wi];
		}
		*OUTPUT++ = sum;
	}
}
