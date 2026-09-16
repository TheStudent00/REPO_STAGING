// probe 226 -- binary /
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_226(uint64_t a, double b)
{
    return a / b;
}
