// probe 851 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_851(double a, bool b)
{
    return a and b;
}
