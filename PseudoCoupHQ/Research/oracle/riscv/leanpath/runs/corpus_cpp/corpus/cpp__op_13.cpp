// probe 13 -- unary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_13(int64_t a)
{
    return -a;
}
