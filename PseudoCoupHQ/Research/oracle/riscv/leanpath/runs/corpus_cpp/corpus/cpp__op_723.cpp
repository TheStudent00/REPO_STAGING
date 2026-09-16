// probe 723 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_723(int64_t a, float b)
{
    return a >> b;
}
