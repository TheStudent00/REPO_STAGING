// probe 59 -- unary --
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_59(bool a)
{
    return --a;
}
