// probe 743 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_743(double a, bool b)
{
    return a >> b;
}
