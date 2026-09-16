// probe 95 -- unary --
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_95(bool a)
{
    return a--;
}
