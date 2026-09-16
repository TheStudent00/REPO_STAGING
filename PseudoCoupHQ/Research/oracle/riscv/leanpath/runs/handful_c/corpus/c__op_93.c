/* probe 93 -- unary ++ */
#include <stdint.h>
#include <stdbool.h>

__typeof__((float){0}++)
op_93(float a)
{
    return a++;
}
