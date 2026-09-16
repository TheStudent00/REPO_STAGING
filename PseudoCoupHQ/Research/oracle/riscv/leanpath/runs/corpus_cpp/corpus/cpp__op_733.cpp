// probe 733 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_733(float a, int64_t b)
{
    return a >> b;
}
