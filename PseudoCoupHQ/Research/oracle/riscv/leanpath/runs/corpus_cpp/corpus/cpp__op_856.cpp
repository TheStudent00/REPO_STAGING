// probe 856 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_856(bool a, double b)
{
    return a and b;
}
