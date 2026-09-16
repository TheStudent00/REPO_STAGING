// probe 997 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_997(bool a, int64_t b)
{
    return a not_eq b;
}
