/* probe 393 -- binary ^ */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int32_t){0} ^ (float){0})
op_393(int32_t a, float b)
{
    return a ^ b;
}
