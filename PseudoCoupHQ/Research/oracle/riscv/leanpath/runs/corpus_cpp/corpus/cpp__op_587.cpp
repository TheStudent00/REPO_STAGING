// probe 587 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_587(uint64_t a, bool b)
{
    return a >= b;
}
