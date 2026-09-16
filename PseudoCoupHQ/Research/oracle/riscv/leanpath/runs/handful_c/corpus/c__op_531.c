/* probe 531 -- binary != */
#include <stdint.h>
#include <stdbool.h>

__typeof__((bool){0} != (float){0})
op_531(bool a, float b)
{
    return a != b;
}
