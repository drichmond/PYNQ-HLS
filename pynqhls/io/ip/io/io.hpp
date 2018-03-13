#ifndef __IO_HPP
#define __IO_HPP

#include "ap_int.h"

#define MEM_SPACE_SIZE 4096
#define REG_SPACE_SIZE 128

#define F_OVERLAY_HZ 50000000ULL
#define MSEC_PER_SEC 1000

void io(const ap_uint<32> mem [MEM_SPACE_SIZE],
	ap_uint<32> reg[REG_SPACE_SIZE],
	const ap_uint<4> buttons,
	ap_uint<4>* leds);

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


#endif
