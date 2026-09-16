// probe 745 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_745(bool a, int64_t b)
{
    return a >> b;
}
