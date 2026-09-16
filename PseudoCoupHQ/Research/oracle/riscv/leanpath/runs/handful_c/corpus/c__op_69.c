/* probe 69 -- unary _alignof */
#include <stdint.h>
#include <stdbool.h>

__typeof__(_alignof (float){0})
op_69(float a)
{
    return _alignof a;
}
