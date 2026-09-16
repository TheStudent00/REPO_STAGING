// probe 183 -- binary *
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_183(int64_t a, float b)
{
    return a * b;
}
