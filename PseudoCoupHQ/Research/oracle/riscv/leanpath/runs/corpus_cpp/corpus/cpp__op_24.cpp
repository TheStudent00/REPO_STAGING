// probe 24 -- unary not
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_24(int32_t a)
{
    return not a;
}
