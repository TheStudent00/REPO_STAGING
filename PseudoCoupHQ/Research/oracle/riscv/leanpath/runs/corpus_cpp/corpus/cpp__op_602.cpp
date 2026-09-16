// probe 602 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_602(bool a, uint64_t b)
{
    return a >= b;
}
