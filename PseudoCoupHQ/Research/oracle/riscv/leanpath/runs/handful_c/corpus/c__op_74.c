/* probe 74 -- unary alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(alignof (uint64_t){0})
op_74(uint64_t a)
{
    return alignof a;
}
