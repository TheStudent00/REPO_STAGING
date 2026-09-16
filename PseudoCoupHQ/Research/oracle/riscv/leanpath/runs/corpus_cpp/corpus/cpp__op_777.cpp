// probe 777 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_777(double a, float b)
{
    return a <=> b;
}
