// probe 664 -- binary <
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_664(float a, double b)
{
    return a < b;
}
