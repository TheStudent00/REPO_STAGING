// probe 993 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_993(double a, float b)
{
    return a not_eq b;
}
