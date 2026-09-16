// probe 977 -- binary not_eq
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_977(int64_t a, bool b)
{
    return a not_eq b;
}
