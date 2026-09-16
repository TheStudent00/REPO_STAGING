// probe 80 -- unary delete
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_80(uint64_t a)
{
    return delete a;
}
