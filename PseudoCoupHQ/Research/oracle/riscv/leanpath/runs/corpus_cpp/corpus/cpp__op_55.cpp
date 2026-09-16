// probe 55 -- unary --
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_55(int64_t a)
{
    return --a;
}
