#include "sfemul.hpp"

namespace sfemul {


uint64_t i32_to_f64_rm0(uint32_t v_arg)
{
    const bool v_i = (v_arg == UINT32_C(0x0));
    const bool v__n7 = (v_i != true);
    const uint64_t v__m8 = (uint64_t)((v__n7) ? ~(uint64_t)0 : (uint64_t)0);
    const uint32_t v__k1 = sf_abs32(v_arg);
    const uint32_t v__k2 = sf_ctlz32(v__k1);
    const uint32_t v_i3 = v__k2;
    const uint64_t v_i12 = (uint64_t)(v__k1);
    const uint32_t v_i4 = (uint32_t)(v_i3 + UINT32_C(0x15));
    const uint32_t v_i8 = (uint32_t)(UINT32_C(0x41d) - v_i3);
    const uint64_t v_i9 = (uint64_t)(v_i8);
    const uint64_t v__sh5 = (uint64_t)((uint64_t)(v_i9) << ((UINT64_C(0x34)) & 63));
    const uint64_t v_i13 = (uint64_t)(v_i4);
    const uint64_t v__sh6 = (uint64_t)((uint64_t)(v_i12) << ((v_i13) & 63));
    const uint64_t v_i14 = v__sh6;
    const uint32_t v__sh3 = (uint32_t)((uint32_t)(v_arg) >> ((UINT32_C(0x1f)) & 31));
    const uint64_t v_i6 = (uint64_t)(v__sh3);
    const uint64_t v__sh4 = (uint64_t)((uint64_t)(v_i6) << ((UINT64_C(0x3f)) & 63));
    const uint64_t v_i11 = (uint64_t)(v__sh5 | v__sh4);
    const uint64_t v_i15 = (uint64_t)(v_i11 + v_i14);
    const uint64_t v__a9 = (uint64_t)(v_i15 & v__m8);
    return v__a9;
}

}  // namespace sfemul
