// probe 91 -- unary --
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_91(int64_t a)
{
    return a--;
}
