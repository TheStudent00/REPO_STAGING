// probe 742 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_742(double a, double b)
{
    return a >> b;
}
