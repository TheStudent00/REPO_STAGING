// probe 706 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_706(double a, double b)
{
    return a << b;
}
