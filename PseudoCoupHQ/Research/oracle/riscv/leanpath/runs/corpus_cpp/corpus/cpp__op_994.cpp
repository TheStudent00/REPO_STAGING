// probe 994 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_994(double a, double b)
{
    return a not_eq b;
}
