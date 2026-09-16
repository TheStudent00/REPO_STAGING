// probe 722 -- binary >>
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_722(int64_t a, uint64_t b)
{
    return a >> b;
}
