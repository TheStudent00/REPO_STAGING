/* probe 3 -- unary ! */
#include <stdint.h>
#include <stdbool.h>

__typeof__(!(float){0})
op_3(float a)
{
    return !a;
}
