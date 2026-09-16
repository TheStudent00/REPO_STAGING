// probe 868 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_868(int64_t a, double b)
{
    return a bitor b;
}
