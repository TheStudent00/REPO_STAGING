// probe 719 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_719(int32_t a, bool b)
{
    return a >> b;
}
