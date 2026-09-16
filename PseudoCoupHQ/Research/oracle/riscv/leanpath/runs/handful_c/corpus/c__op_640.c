/* probe 640 -- binary <= */
#include <stdint.h>
#include <stdbool.h>

__typeof__((bool){0} <= (double){0})
op_640(bool a, double b)
{
    return a <= b;
}
