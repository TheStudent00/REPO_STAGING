#include "sfemul.hpp"

namespace sfemul {


bool f32_lt_rm1(uint64_t v_arg, uint64_t v_arg1)
{
    const uint32_t v_i = (uint32_t)(v_arg);
    const uint32_t v_i2 = (uint32_t)(v_arg1);
    const uint32_t v_i3 = (uint32_t)(v_i & UINT32_C(0x7f800000));
    const bool v_i4 = (v_i3 != UINT32_C(0x7f800000));
    const uint32_t v_i5 = (uint32_t)(v_i & UINT32_C(0x7fffff));
    const bool v_i6 = (v_i5 == UINT32_C(0x0));
    const bool v_i7 = (v_i4 || v_i6);
    const uint32_t v_i9 = (uint32_t)(v_i2 & UINT32_C(0x7f800000));
    const bool v_i10 = (v_i9 != UINT32_C(0x7f800000));
    const uint32_t v_i11 = (uint32_t)(v_i2 & UINT32_C(0x7fffff));
    const bool v_i12 = (v_i11 == UINT32_C(0x0));
    const bool v_i13 = (v_i10 || v_i12);
    const bool v__c5 = (v_i7 && v_i13);
    const uint32_t v_i15 = (uint32_t)(v_i2 ^ v_i);
    const bool v_i16 = ((int32_t)(v_i15) > INT32_C(-1));
    const bool v_i18 = ((int32_t)(v_i) < INT32_C(0));
    const uint32_t v_i19 = (uint32_t)(v_i2 | v_i);
    const uint32_t v_i20 = (uint32_t)(v_i19 & UINT32_C(0x7fffffff));
    const bool v_i21 = (v_i20 != UINT32_C(0x0));
    const bool v_i22 = (v_i18 && v_i21);
    const bool v_i24 = (v_i != v_i2);
    const bool v_i25 = (v_i < v_i2);
    const bool v_i27 = (v_i18 != v_i25);
    const bool v_i28 = (v_i24 && v_i27);
    const bool v__a3 = (v_i28 && v_i16);
    const bool v__n1 = (v_i16 != true);
    const bool v__a2 = (v_i22 && v__n1);
    const bool v__o4 = (v__a2 || v__a3);
    const bool v__a6 = (v__o4 && v__c5);
    return v__a6;
}

}  // namespace sfemul
