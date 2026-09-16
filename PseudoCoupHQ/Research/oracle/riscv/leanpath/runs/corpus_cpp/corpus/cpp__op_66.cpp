// probe 66 -- unary co_await
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_66(int32_t a)
{
    return co_await a;
}
