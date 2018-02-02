#ifndef __FILT1D_HPP
#define __FILT1D_HPP

#define C_NUM_COEFF 9
#include "ap_int.h"

struct axis_t {
	int data;
	ap_int<1> last;
};

void filt1d(axis_t *INPUT, axis_t *OUTPUT,
		int coeff[C_NUM_COEFF], unsigned int length);

#endif
