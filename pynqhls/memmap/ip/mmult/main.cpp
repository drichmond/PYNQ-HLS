#include "mmult.hpp"
#include <random>
#include <stdio.h>
#include "hls_linear_algebra.h"

int main(){
	// Declare Data-Input Matricies
	// Matrix B is transposed for efficient memory accesses
	mata_t A[A_ROWS][A_COLS];
	matb_t BT[B_COLS][B_ROWS];
	// Declare Data-Output Matrices
	// C is the output of the HLS core
	// CG is the output of the HLS Library Function (C-Gold)
	matc_t C[A_ROWS][B_COLS];
	matc_t CG[A_ROWS][B_COLS];	

	// Generate some randomness
	std::default_random_engine generator;
	std::uniform_int_distribution<int> distribution(RN_MIN,RN_MAX);

	// Generate Matrix A from a uniform real distribution
	for(unsigned int i = 0; i < A_ROWS; ++i){
		for(unsigned int j = 0; j < A_COLS; ++j){
			mata_t rn = static_cast<mata_t>(distribution(generator));
			A[i][j] = rn;
		}
	}

	// Generate Matrix B (Transpose) from a uniform real distribution
	for(unsigned int j = 0; j < B_COLS; ++j){
		for(unsigned int i = 0; i < B_ROWS; ++i){
			mata_t rn = static_cast<matb_t>(distribution(generator));
			BT[j][i] = rn;
		}
	}

	// Call the Synthesizable Matrix Multiply function (mmult)
	mmult(A, BT, C);

	// Call the HLS-library matrix multiply to generate 'gold' data
	hls::matrix_multiply <hls::NoTranspose, hls::Transpose,
			      A_ROWS, A_COLS,
			      B_ROWS, B_COLS,
			      A_ROWS, B_COLS,
			      mata_t, matc_t>
		(A, BT, CG);

	// If PRINTMAT is defined, call the matrix printing functions

#ifdef PRINTMAT
	printf("A = \n");
	hls::print_matrix<A_ROWS, A_COLS, mata_t, hls::NoTranspose>(A, "   ");

	printf("B = \n");
	hls::print_matrix<B_COLS, B_ROWS, matb_t, hls::Transpose>(BT, "   ");

	printf("C = \n");
	hls::print_matrix<A_ROWS, B_COLS, matc_t, hls::NoTranspose>(C, "   ");

	printf("CG = \n");
	hls::print_matrix<A_ROWS, B_COLS, matc_t, hls::NoTranspose>(CG, "   ");
#endif

	// Compute the SSE of the matrix multiply functions
	double sse= 0;
	for(unsigned int i = 0; i < A_ROWS; ++i){
		for(unsigned int j = 0; j < B_COLS; ++j){
			double delta = C[i][j] - CG[i][j];
			sse += delta*delta;
		}
	}

	if(sse > SSE_MAX){
		printf("Failure: Sum of squared error (SSE) is greater than %f",
			SSE_MAX);
		return 1;
	}

	return 0;
}
