// probe 389 -- binary |
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_389(bool a, bool b)
{
    return a | b;
}
