#include "vvadd.hpp"
#include <random>
#include <stdio.h>

#define DTYPE int
#define LENGTH 1024
int main(){

	// Generate some randomness
	std::default_random_engine generator;
	std::uniform_int_distribution<int> distribution(-1000,1000);

	int l[LENGTH], r[LENGTH], soln[LENGTH], out[LENGTH];
	
	for(unsigned int i = 0; i < LENGTH; ++i){
		int rn = distribution(generator);
		l[i] = rn;
		rn = distribution(generator);
		r[i] = rn;
	}
	
	for(unsigned int i = 0; i < LENGTH; ++i){
		soln[i] = l[i] + r[i];
	}
	
	vvadd(l, r, out, LENGTH, 0, 0, 0);
	
	for(unsigned int i = 0; i < LENGTH; ++i){
		printf("Soln: %d, Result: %d\n", soln[i], out[i]);
		if(soln[i] != out[i]){
			printf("Error! Incorrect result on index %u. Soln: %d, Result: %d\n", i, soln[i], out[i]);
			return -1;
		}
	}
	
	return 0;
}
