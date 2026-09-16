// probe 72 -- unary new
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_72(int32_t a)
{
    return new a;
}
