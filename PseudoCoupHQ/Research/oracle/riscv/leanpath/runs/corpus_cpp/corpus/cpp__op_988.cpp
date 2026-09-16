// probe 988 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_988(float a, double b)
{
    return a not_eq b;
}
