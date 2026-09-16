// probe 544 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_544(int64_t a, double b)
{
    return a > b;
}
