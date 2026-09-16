// probe 71 -- unary co_await
#include <cstdint>
#include <compare>
#include <new>

extern "C" auto
op_71(bool a)
{
    return co_await a;
}
