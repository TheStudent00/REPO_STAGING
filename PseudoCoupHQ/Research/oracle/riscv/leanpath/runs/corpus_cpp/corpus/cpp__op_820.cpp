// probe 820 -- binary or
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_820(bool a, double b)
{
    return a or b;
}
