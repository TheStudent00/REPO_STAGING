// probe 744 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_744(bool a, int32_t b)
{
    return a >> b;
}
