// probe 242 -- binary /
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_242(bool a, uint64_t b)
{
    return a / b;
}
