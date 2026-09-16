// probe 19 -- unary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_19(int64_t a)
{
    return +a;
}
