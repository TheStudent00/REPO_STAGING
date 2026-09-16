// probe 98 -- unary ...
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_98(uint64_t a)
{
    return a...;
}
