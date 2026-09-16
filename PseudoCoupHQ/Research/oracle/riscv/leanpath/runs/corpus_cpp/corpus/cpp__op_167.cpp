// probe 167 -- binary -
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_167(double a, bool b)
{
    return a - b;
}
