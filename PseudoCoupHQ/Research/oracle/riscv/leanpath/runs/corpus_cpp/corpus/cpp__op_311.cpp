// probe 311 -- binary ||
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_311(double a, bool b)
{
    return a || b;
}
