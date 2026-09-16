// probe 641 -- binary <=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_641(bool a, bool b)
{
    return a <= b;
}
