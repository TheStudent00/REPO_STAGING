// probe 605 -- binary >=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_605(bool a, bool b)
{
    return a >= b;
}
