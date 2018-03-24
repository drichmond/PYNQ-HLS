#include "mmult.hpp"

// mmult()
//     Implements a simple matrix-multiply function in HLS
// Parameters:
//     A - mata_t
//         A 2-dimensional array of mata_t values to be multiplied
//                  
//     BT - matb_t
//         A 2-dimensional array of matb_t values to be multiplied
//         BT is the transpose of B
//
//     C - matc_t
//         Matrix multiply output definition
// 
// The dimensions of the arrays are defined in mmult.hpp.
void mmult(const mata_t A [A_ROWS][A_COLS],
	const matb_t BT [B_COLS][B_ROWS],
	matc_t C [A_ROWS][B_COLS]){
/* Define a new AXI-Lite bus named CTRL for offset arguments, and HLS
   Status/Control registers (return)*/
#pragma HLS INTERFACE s_axilite port=return bundle=CTRL
/* Define a new AXI4 Master bus named DATA for memory ports A, BT, and C.  The
   argument offset=slave specifies that the the pointers (offset) of A, BT, and
   C can be set using register writes in the CTRL axi slave port */
#pragma HLS INTERFACE m_axi port=A offset=slave bundle=DATA
#pragma HLS INTERFACE m_axi port=BT offset=slave bundle=DATA
#pragma HLS INTERFACE m_axi port=C offset=slave bundle=DATA

	// We use the log2 functions in mmult.hpp to determine the correct size
	// of the index variables i, j, and k. Typically, vivado will size these
	// correctly
	ap_uint<pynq::log2(A_ROWS) + 1> i = 0;
	ap_uint<pynq::log2(B_COLS) + 1> j = 0;
	ap_uint<pynq::log2(A_COLS) + 1> k = 0;

	// Perform a simple matrix-multiply with three nested for-loops
	for(i = 0; i < A_ROWS; ++i){
		for(j = 0; j < B_COLS; ++j){
			matc_t sum = 0;
			for(k = 0; k < A_ROWS; ++k){
#pragma HLS PIPELINE
				sum += A[i][k]*BT[j][k];
			}
			C[i][j] = sum;
		}
	}
}
