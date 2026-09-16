// probe 68 -- unary co_await
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_68(uint64_t a)
{
    return co_await a;
}
