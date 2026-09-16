// probe 784 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_784(bool a, double b)
{
    return a <=> b;
}
