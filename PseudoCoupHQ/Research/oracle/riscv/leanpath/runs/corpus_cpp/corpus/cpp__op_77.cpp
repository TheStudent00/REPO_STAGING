// probe 77 -- unary new
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_77(bool a)
{
    return new a;
}
