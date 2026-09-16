// probe 52 -- unary ++
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_52(double a)
{
    return ++a;
}
