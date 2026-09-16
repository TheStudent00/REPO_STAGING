// probe 14 -- unary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_14(uint64_t a)
{
    return -a;
}
