// probe 737 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_737(float a, bool b)
{
    return a >> b;
}
