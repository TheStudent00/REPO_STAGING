#include "sfemul.hpp"

namespace sfemul {


bool f16_lt_quiet_rm1(uint64_t v_arg, uint64_t v_arg1)
{
    const uint32_t v_i = (uint32_t)(v_arg);
    const uint32_t v_i2 = (uint32_t)(v_i & UINT32_C(0xffff));
    const uint32_t v_i3 = (uint32_t)(v_arg1);
    const uint32_t v_i4 = (uint32_t)(v_i3 & UINT32_C(0xffff));
    const uint32_t v_i5 = (uint32_t)(v_i & UINT32_C(0x7c00));
    const bool v_i6 = (v_i5 != UINT32_C(0x7c00));
    const uint32_t v_i7 = (uint32_t)(v_i & UINT32_C(0x3ff));
    const bool v_i8 = (v_i7 == UINT32_C(0x0));
    const bool v_i9 = (v_i6 || v_i8);
    const uint32_t v_i21 = (uint32_t)(v_i3 | v_i);
    const uint32_t v_i22 = (uint32_t)(v_i21 & UINT32_C(0x7fff));
    const bool v_i23 = (v_i22 != UINT32_C(0x0));
    const uint32_t v_i11 = (uint32_t)(v_i3 & UINT32_C(0x7c00));
    const bool v_i12 = (v_i11 != UINT32_C(0x7c00));
    const uint32_t v_i13 = (uint32_t)(v_i3 & UINT32_C(0x3ff));
    const bool v_i14 = (v_i13 == UINT32_C(0x0));
    const bool v_i15 = (v_i12 || v_i14);
    const bool v__c5 = (v_i9 && v_i15);
    const bool v_i17 = (v_i2 > UINT32_C(0x7fff));
    const bool v_i24 = (v_i17 && v_i23);
    const bool v_i18 = (v_i4 < UINT32_C(0x8000));
    const bool v_i19 = (v_i17 != v_i18);
    const bool v_i26 = (v_i2 != v_i4);
    const bool v_i27 = (v_i2 < v_i4);
    const bool v_i28 = (v_i17 != v_i27);
    const bool v_i29 = (v_i26 && v_i28);
    const bool v__a3 = (v_i29 && v_i19);
    const bool v__n1 = (v_i19 != true);
    const bool v__a2 = (v_i24 && v__n1);
    const bool v__o4 = (v__a2 || v__a3);
    const bool v__a6 = (v__o4 && v__c5);
    return v__a6;
}

}  // namespace sfemul
