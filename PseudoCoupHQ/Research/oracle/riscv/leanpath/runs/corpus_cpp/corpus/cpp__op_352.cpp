// probe 352 -- binary &&
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_352(bool a, double b)
{
    return a && b;
}
