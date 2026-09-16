/* probe 27 -- unary * */
#include <stdint.h>
#include <stdbool.h>

__typeof__(*(float){0})
op_27(float a)
{
    return *a;
}
