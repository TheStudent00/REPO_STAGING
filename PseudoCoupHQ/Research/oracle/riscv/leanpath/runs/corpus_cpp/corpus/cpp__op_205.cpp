// probe 205 -- binary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_205(bool a, int64_t b)
{
    return a * b;
}
