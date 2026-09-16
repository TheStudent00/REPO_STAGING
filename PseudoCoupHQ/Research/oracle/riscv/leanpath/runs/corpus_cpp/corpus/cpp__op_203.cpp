// probe 203 -- binary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_203(double a, bool b)
{
    return a * b;
}
