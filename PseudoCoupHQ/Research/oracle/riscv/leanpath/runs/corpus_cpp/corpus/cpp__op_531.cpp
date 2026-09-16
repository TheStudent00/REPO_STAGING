// probe 531 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_531(bool a, float b)
{
    return a != b;
}
