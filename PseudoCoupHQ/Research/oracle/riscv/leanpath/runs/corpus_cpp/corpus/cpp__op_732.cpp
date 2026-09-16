// probe 732 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_732(float a, int32_t b)
{
    return a >> b;
}
