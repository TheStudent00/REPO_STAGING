// probe 503 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_503(int32_t a, bool b)
{
    return a != b;
}
