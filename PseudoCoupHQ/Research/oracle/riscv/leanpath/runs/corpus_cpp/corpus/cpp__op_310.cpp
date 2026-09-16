// probe 310 -- binary ||
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_310(double a, double b)
{
    return a || b;
}
