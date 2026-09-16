// probe 497 -- binary ==
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_497(bool a, bool b)
{
    return a == b;
}
