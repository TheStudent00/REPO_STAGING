/* probe 556 -- binary > */
#include <stdint.h>
#include <stdbool.h>

__typeof__((float){0} > (double){0})
op_556(float a, double b)
{
    return a > b;
}
