// probe 530 -- binary !=
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_530(bool a, uint64_t b)
{
    return a != b;
}
