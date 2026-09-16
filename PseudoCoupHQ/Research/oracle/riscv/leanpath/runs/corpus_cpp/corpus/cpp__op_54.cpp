// probe 54 -- unary --
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_54(int32_t a)
{
    return --a;
}
