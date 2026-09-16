// probe 936 -- binary bitand
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_936(int64_t a, int32_t b)
{
    return a bitand b;
}
