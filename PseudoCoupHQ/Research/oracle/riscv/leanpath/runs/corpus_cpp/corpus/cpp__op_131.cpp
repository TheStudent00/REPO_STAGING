// probe 131 -- binary +
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_131(double a, bool b)
{
    return a + b;
}
