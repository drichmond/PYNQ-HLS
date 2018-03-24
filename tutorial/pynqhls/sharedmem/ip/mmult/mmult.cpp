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

	// Your code goes here!

}
