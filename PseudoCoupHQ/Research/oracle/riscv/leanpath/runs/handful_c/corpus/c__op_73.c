/* probe 73 -- unary alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(alignof (int64_t){0})
op_73(int64_t a)
{
    return alignof a;
}
