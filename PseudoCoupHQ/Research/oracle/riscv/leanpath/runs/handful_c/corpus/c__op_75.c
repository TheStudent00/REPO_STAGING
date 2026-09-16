/* probe 75 -- unary alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(alignof (float){0})
op_75(float a)
{
    return alignof a;
}
