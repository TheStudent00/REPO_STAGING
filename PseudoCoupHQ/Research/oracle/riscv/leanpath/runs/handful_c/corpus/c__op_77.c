/* probe 77 -- unary alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(alignof (bool){0})
op_77(bool a)
{
    return alignof a;
}
