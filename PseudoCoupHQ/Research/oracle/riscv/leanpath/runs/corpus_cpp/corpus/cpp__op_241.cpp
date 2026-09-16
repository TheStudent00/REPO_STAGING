// probe 241 -- binary /
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_241(bool a, int64_t b)
{
    return a / b;
}
