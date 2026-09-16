// probe 208 -- binary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_208(bool a, double b)
{
    return a * b;
}
