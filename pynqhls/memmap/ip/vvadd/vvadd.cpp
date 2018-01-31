#include "vvadd.hpp"

void vvadd(int *L, int *R, int *OUTPUT, unsigned int length, 
	int loffset, int roffset, int ooffset){
#pragma HLS INTERFACE m_axi port=L depth=1073741824
#pragma HLS INTERFACE m_axi port=R depth=1073741824
#pragma HLS INTERFACE m_axi port=OUTPUT depth=1073741824
#pragma HLS INTERFACE s_axilite port=length bundle=CTRL
#pragma HLS INTERFACE s_axilite port=loffset bundle=CTRL
#pragma HLS INTERFACE s_axilite port=roffset bundle=CTRL
#pragma HLS INTERFACE s_axilite port=ooffset bundle=CTRL
#pragma HLS INTERFACE s_axilite port=return bundle=CTRL
	for (unsigned int i = 0 ; i < length; i++) {
#pragma HLS PIPELINE
		OUTPUT[i + ooffset] = L[i + loffset] + R[i + roffset];
	}
}
