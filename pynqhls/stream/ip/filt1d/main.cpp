#include "filt1d.hpp"
#include <random>
#include <stdio.h>

#define DTYPE int
#define LENGTH 100
int main(){

	// Generate some randomness
	std::default_random_engine generator;
	std::uniform_int_distribution<int> distribution(-1000,1000);

	int input[LENGTH];
	int soln[LENGTH];
	int window[C_NUM_COEFF] = {0};
	int coeffs[C_NUM_COEFF] = {-4, -3, -2, -1, 0, 1, 2, 3, 4};
	int sum;
	int in[LENGTH];
	int out[LENGTH];
	
	for(unsigned int i = 0; i < LENGTH; ++i){
		int rn = distribution(generator);
		input[i] = rn;
		in[i] = rn;
	}
	
	for(unsigned int i = 0; i < LENGTH; ++i){
		sum = 0;
		for(unsigned int wi = C_NUM_COEFF-1; wi > 0; --wi){
			window[wi] = window[wi - 1];
		}
		window[0] = input[i];
		for(unsigned int wi = 0; wi < C_NUM_COEFF; ++wi){
			sum += window[wi]* coeffs[wi];
		}
		soln[i] = sum;
	}
	
	filt1d(in, out, coeffs, LENGTH);
	
	for(unsigned int i = 0; i < LENGTH; ++i){
		printf("Soln: %d, Result: %d\n", soln[i], out[i]);
		if(soln[i] != out[i]){
			printf("Error! Incorrect result on index %u. Soln: %d, Result: %d\n", i, soln[i], out[i]);
			return -1;
		}
	}
	
	return 0;
}
