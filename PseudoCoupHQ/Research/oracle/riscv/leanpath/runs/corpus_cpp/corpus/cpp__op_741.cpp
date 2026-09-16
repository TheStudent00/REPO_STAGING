// probe 741 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_741(double a, float b)
{
    return a >> b;
}
