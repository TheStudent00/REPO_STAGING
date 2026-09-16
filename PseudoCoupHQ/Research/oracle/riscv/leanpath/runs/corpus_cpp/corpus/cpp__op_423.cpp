// probe 423 -- binary ^
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_423(bool a, float b)
{
    return a ^ b;
}
