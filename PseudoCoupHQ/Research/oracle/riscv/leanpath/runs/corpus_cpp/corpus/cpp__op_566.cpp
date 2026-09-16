// probe 566 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_566(bool a, uint64_t b)
{
    return a > b;
}
