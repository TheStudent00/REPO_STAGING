/* probe 495 -- binary == */
#include <stdint.h>
#include <stdbool.h>

__typeof__((bool){0} == (float){0})
op_495(bool a, float b)
{
    return a == b;
}
