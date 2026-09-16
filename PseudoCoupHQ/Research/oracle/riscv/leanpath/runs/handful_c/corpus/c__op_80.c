/* probe 80 -- unary _Alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(_Alignof (uint64_t){0})
op_80(uint64_t a)
{
    return _Alignof a;
}
