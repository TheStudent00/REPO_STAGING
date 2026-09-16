// probe 853 -- binary and
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_853(bool a, int64_t b)
{
    return a and b;
}
