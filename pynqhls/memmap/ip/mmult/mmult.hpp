#ifndef __FILT1D_HPP
#define __FILT1D_HPP

#include "ap_int.h"

// Matrix Definitions:
//     Types for A (mata_t), B (matb_t), and C (matc_t)
typedef float mata_t;
typedef float matb_t;
typedef float matc_t;
// Dimensions for A and B (which determine C)
#define A_ROWS 100
#define A_COLS 100
#define B_ROWS A_COLS
#define B_COLS 100

// Testbench definitions
// Min and Max numbers for the Random Number Generator
#define RN_MIN -1
#define RN_MAX 1
// Maximum Sum of Squared Error
#define SSE_MAX .1

// For convenience, we define a log2, and clog2 function that is a constexpr
// This is useful for computing the size of index variables (though it usually
// isnt necessary)
namespace pynq {
	constexpr std::size_t log2(std::size_t n)
	{
		return ((n <= 2) ? 1 : 1 + log2(n / 2));
	}

	constexpr std::size_t clog2(std::size_t n)
	{
		return log2(n) + (n > (1 << log2(n)));
	}
}

// mmult()
//     Implements a simple matrix-multiply function in HLS
// Parameters:
//     A - mata_t
//         A 2-dimensional array of mata_t values to be multiplied
//                  
//     BT - matb_t
//         A 2-dimensional array of matb_t values to be multiplied
//         BT is the transposes of B
//
//     C - matc_t
//         Matrix multiply output definition
// 
// The dimensions of the arrays are defined above.
void mmult(const mata_t A [A_ROWS][A_COLS],
	const matb_t BT [B_COLS][B_ROWS],
	matc_t C [A_ROWS][B_COLS]);

#endif
