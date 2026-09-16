// probe 857 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_857(bool a, bool b)
{
    return a and b;
}
