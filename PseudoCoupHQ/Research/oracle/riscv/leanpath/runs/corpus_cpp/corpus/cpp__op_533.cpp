// probe 533 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_533(bool a, bool b)
{
    return a != b;
}
