// probe 67 -- unary co_await
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_67(int64_t a)
{
    return co_await a;
}
