// probe 890 -- binary bitor
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_890(bool a, uint64_t b)
{
    return a bitor b;
}
