// probe 701 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_701(float a, bool b)
{
    return a << b;
}
