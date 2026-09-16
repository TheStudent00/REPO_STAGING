// probe 603 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_603(bool a, float b)
{
    return a >= b;
}
