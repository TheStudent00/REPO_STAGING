// probe 867 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_867(int64_t a, float b)
{
    return a bitor b;
}
