// probe 725 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_725(int64_t a, bool b)
{
    return a >> b;
}
