// probe 850 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_850(double a, double b)
{
    return a and b;
}
