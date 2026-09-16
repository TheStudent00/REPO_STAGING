/* probe 389 -- binary | */
#include <stdint.h>
#include <stdbool.h>

__typeof__((bool){0} | (bool){0})
op_389(bool a, bool b)
{
    return a | b;
}
