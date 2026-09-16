// probe 347 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_347(double a, bool b)
{
    return a && b;
}
