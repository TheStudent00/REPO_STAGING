// probe 88 -- unary ++
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_88(double a)
{
    return a++;
}
