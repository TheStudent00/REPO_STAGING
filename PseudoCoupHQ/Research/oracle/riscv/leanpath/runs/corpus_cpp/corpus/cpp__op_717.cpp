// probe 717 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_717(int32_t a, float b)
{
    return a >> b;
}
