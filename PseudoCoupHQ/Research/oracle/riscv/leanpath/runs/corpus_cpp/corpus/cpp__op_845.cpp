// probe 845 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_845(float a, bool b)
{
    return a and b;
}
