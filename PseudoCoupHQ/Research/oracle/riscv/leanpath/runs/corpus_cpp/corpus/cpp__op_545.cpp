// probe 545 -- binary >
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_545(int64_t a, bool b)
{
    return a > b;
}
