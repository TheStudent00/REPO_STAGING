// probe 863 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_863(int32_t a, bool b)
{
    return a bitor b;
}
