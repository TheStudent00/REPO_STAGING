// probe 202 -- binary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_202(double a, double b)
{
    return a * b;
}
