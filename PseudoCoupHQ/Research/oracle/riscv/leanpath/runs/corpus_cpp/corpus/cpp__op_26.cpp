// probe 26 -- unary not
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_26(uint64_t a)
{
    return not a;
}
