// probe 1 -- unary !
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_1(int64_t a)
{
    return !a;
}
