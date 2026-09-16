// probe 424 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_424(bool a, double b)
{
    return a ^ b;
}
