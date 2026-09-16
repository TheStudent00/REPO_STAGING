// probe 407 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_407(uint64_t a, bool b)
{
    return a ^ b;
}
