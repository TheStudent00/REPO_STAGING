// probe 87 -- unary ++
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_87(float a)
{
    return a++;
}
