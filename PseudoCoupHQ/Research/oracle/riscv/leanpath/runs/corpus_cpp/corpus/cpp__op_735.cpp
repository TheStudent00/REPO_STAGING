// probe 735 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_735(float a, float b)
{
    return a >> b;
}
