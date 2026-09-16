// probe 712 -- binary <<
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_712(bool a, double b)
{
    return a << b;
}
