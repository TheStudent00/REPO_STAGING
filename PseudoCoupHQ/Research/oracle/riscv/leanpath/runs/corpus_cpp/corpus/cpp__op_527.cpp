// probe 527 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_527(double a, bool b)
{
    return a != b;
}
