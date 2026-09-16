// probe 79 -- unary delete
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_79(int64_t a)
{
    return delete a;
}
