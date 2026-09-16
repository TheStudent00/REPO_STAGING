// probe 78 -- unary delete
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_78(int32_t a)
{
    return delete a;
}
