#ifndef __FILT1D_HPP
#define __FILT1D_HPP

#define C_NUM_COEFF 9
#include "ap_int.h"
#include "ap_axi_sdata.h"
void filt1d(int *INPUT, int *OUTPUT,
		int coeff[C_NUM_COEFF], unsigned int length);

#endif
