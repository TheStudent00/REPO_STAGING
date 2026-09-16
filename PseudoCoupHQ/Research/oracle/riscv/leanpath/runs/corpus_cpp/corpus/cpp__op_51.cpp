// probe 51 -- unary ++
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_51(float a)
{
    return ++a;
}
