/* probe 72 -- unary alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(alignof (int32_t){0})
op_72(int32_t a)
{
    return alignof a;
}
