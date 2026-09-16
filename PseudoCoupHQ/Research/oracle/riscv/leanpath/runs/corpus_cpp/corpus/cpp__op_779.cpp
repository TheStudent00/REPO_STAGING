// probe 779 -- binary <=>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_779(double a, bool b)
{
    return a <=> b;
}
