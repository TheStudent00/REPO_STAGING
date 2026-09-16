#include "sfemul.hpp"

namespace sfemul {


uint64_t f64_roundToInt_rm1(uint64_t v_arg, bool v_arg1)
{
    const uint64_t v_i = (uint64_t)((uint64_t)(v_arg) >> ((UINT64_C(0x34)) & 63));
    const uint32_t v_i2 = (uint32_t)(v_i);
    const uint32_t v_i3 = (uint32_t)(v_i2 & UINT32_C(0x7ff));
    const bool v_i4 = (v_i3 < UINT32_C(0x3ff));
    const uint64_t v_i6 = (uint64_t)(v_arg & UINT64_C(0x7fffffffffffffff));
    const bool v_i7 = (v_i6 == UINT64_C(0x0));
    const uint64_t v__m1 = (uint64_t)((v_i7) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v_i8 = (uint64_t)(v_arg & UINT64_C(0x8000000000000000));
    const uint64_t v__a2 = (uint64_t)(v_arg & v__m1);
    const uint64_t v__n3 = (uint64_t)(v__m1 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v__a4 = (uint64_t)(v_i8 & v__n3);
    const uint64_t v_spec_select = (uint64_t)(v__a2 | v__a4);
    const bool v_i10 = (v_i3 > UINT32_C(0x432));
    const bool v_i12 = (v_i3 != UINT32_C(0x7ff));
    const uint32_t v_i17 = (uint32_t)(UINT32_C(0x433) - v_i3);
    const uint64_t v_i18 = (uint64_t)(v_i17);
    const uint64_t v__sh9 = (uint64_t)((uint64_t)(UINT64_C(0xffffffffffffffff)) << ((v_i18) & 63));
    const uint64_t v__neg = v__sh9;
    const uint64_t v_i19 = (uint64_t)(v_arg & v__neg);
    const uint64_t v_i13 = (uint64_t)(v_arg & UINT64_C(0xfffffffffffff));
    const bool v_i14 = (v_i13 == UINT64_C(0x0));
    const bool v_i15 = (v_i14 || v_i12);
    const uint64_t v__m5 = (uint64_t)((v_i15) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a6 = (uint64_t)(v_arg & v__m5);
    const uint64_t v__n7 = (uint64_t)(v__m5 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v__a8 = (uint64_t)(UINT64_C(0x7ff8000000000000) & v__n7);
    const uint64_t v_spec_select4 = (uint64_t)(v__a6 | v__a8);
    const bool v__n10 = (v_i10 != true);
    const bool v__n11 = (v_i4 != true);
    const bool v__c12 = (v__n10 && v__n11);
    const uint64_t v__m13 = (uint64_t)((v__c12) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a14 = (uint64_t)(v_i19 & v__m13);
    const uint64_t v__m15 = (uint64_t)((v_i4) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a16 = (uint64_t)(v_spec_select & v__m15);
    const uint64_t v__o17 = (uint64_t)(v__a14 | v__a16);
    const uint64_t v__m19 = (uint64_t)((v_i10) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a20 = (uint64_t)(v_spec_select4 & v__m19);
    const uint64_t v__o21 = (uint64_t)(v__o17 | v__a20);
    return v__o21;
}

}  // namespace sfemul
