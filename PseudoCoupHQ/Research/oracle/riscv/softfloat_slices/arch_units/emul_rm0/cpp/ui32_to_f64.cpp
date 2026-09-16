#include "sfemul.hpp"

namespace sfemul {


uint64_t ui32_to_f64_rm0(uint32_t v_arg)
{
    const bool v_i = (v_arg == UINT32_C(0x0));
    const bool v__n4 = (v_i != true);
    const uint64_t v__m5 = (uint64_t)((v__n4) ? ~(uint64_t)0 : (uint64_t)0);
    const uint32_t v__k1 = sf_ctlz32(v_arg);
    const uint32_t v_i2 = v__k1;
    const uint32_t v_i3 = (uint32_t)(v_i2 + UINT32_C(0x15));
    const uint32_t v_i4 = (uint32_t)(UINT32_C(0x41d) - v_i2);
    const uint64_t v_i5 = (uint64_t)(v_i4);
    const uint64_t v__sh2 = (uint64_t)((uint64_t)(v_i5) << ((UINT64_C(0x34)) & 63));
    const uint64_t v_i8 = (uint64_t)(v_i3);
    const uint64_t v_i7 = (uint64_t)(v_arg);
    const uint64_t v__sh3 = (uint64_t)((uint64_t)(v_i7) << ((v_i8) & 63));
    const uint64_t v_i9 = v__sh3;
    const uint64_t v_i10 = (uint64_t)(v__sh2 + v_i9);
    const uint64_t v__a6 = (uint64_t)(v_i10 & v__m5);
    return v__a6;
}

}  // namespace sfemul
