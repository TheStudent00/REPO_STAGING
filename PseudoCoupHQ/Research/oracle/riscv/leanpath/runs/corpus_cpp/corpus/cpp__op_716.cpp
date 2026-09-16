// probe 716 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_716(int32_t a, uint64_t b)
{
    return a >> b;
}
