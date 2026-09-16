// probe 179 -- binary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_179(int32_t a, bool b)
{
    return a * b;
}
