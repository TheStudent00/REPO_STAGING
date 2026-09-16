#include "sfemul.hpp"

namespace sfemul {


uint64_t f64_roundToInt_rm0(uint64_t v_arg, bool v_arg1)
{
    const uint64_t v_i = (uint64_t)((uint64_t)(v_arg) >> ((UINT64_C(0x34)) & 63));
    const uint32_t v_i2 = (uint32_t)(v_i);
    const uint32_t v_i3 = (uint32_t)(v_i2 & UINT32_C(0x7ff));
    const bool v_i4 = (v_i3 < UINT32_C(0x3ff));
    const bool v_i16 = (v_i3 > UINT32_C(0x432));
    const uint64_t v_i6 = (uint64_t)(v_arg & UINT64_C(0x7fffffffffffffff));
    const bool v_i7 = (v_i6 == UINT64_C(0x0));
    const bool v_i18 = (v_i3 != UINT32_C(0x7ff));
    const uint64_t v_i19 = (uint64_t)(v_arg & UINT64_C(0xfffffffffffff));
    const bool v_i20 = (v_i19 == UINT64_C(0x0));
    const bool v_i21 = (v_i20 || v_i18);
    const uint64_t v__m1 = (uint64_t)((v_i21) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a2 = (uint64_t)(v_arg & v__m1);
    const uint64_t v__n3 = (uint64_t)(v__m1 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v__a4 = (uint64_t)(UINT64_C(0x7ff8000000000000) & v__n3);
    const uint64_t v_spec_select4 = (uint64_t)(v__a2 | v__a4);
    const uint32_t v_i23 = (uint32_t)(UINT32_C(0x433) - v_i3);
    const uint64_t v_i24 = (uint64_t)(v_i23);
    const uint64_t v__sh5 = (uint64_t)((uint64_t)(UINT64_C(0x1)) << ((v_i24) & 63));
    const uint64_t v_i25 = v__sh5;
    const bool v_i12 = (v_i3 == UINT32_C(0x3fe));
    const uint64_t v_i26 = (uint64_t)(v_i25 + UINT64_C(0xffffffffffffffff));
    const uint64_t v__sh6 = (uint64_t)((uint64_t)(v_i25) >> ((UINT64_C(0x1)) & 63));
    const uint64_t v_i28 = (uint64_t)(v__sh6 + v_arg);
    const uint64_t v_i29 = (uint64_t)(v_i28 & v_i26);
    const bool v_i30 = (v_i29 == UINT64_C(0x0));
    const uint64_t v__m7 = (uint64_t)((v_i30) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v_i31 = (uint64_t)(v_i25 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v__a8 = (uint64_t)(v_i31 & v__m7);
    const uint64_t v__n9 = (uint64_t)(v__m7 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v_i32 = (uint64_t)(v__a8 | v__n9);
    const uint64_t v_i33 = (uint64_t)(UINT64_C(0x0) - v_i25);
    const uint64_t v_i34 = (uint64_t)(v_i32 & v_i33);
    const uint64_t v_i35 = (uint64_t)(v_i34 & v_i28);
    const uint64_t v_i9 = (uint64_t)(v_arg & UINT64_C(0x8000000000000000));
    const bool v_i11 = (v_i19 != UINT64_C(0x0));
    const bool v_i13 = (v_i11 && v_i12);
    const uint64_t v__m11 = (uint64_t)((v_i13) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v_i14 = (uint64_t)(v_i9 | UINT64_C(0x3ff0000000000000));
    const uint64_t v__a12 = (uint64_t)(v_i14 & v__m11);
    const uint64_t v__n13 = (uint64_t)(v__m11 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v__a14 = (uint64_t)(v_i9 & v__n13);
    const uint64_t v_spec_select = (uint64_t)(v__a12 | v__a14);
    const bool v__c15 = (v_i7 && v_i4);
    const uint64_t v__m16 = (uint64_t)((v__c15) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a17 = (uint64_t)(v_arg & v__m16);
    const bool v__n18 = (v_i7 != true);
    const bool v__c19 = (v__n18 && v_i4);
    const uint64_t v__m20 = (uint64_t)((v__c19) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a21 = (uint64_t)(v_spec_select & v__m20);
    const uint64_t v__o22 = (uint64_t)(v__a17 | v__a21);
    const bool v__n23 = (v_i4 != true);
    const bool v__n24 = (v_i16 != true);
    const bool v__c25 = (v__n23 && v__n24);
    const uint64_t v__m26 = (uint64_t)((v__c25) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a27 = (uint64_t)(v_i35 & v__m26);
    const uint64_t v__o28 = (uint64_t)(v__o22 | v__a27);
    const uint64_t v__m30 = (uint64_t)((v_i16) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a31 = (uint64_t)(v_spec_select4 & v__m30);
    const uint64_t v__o32 = (uint64_t)(v__o28 | v__a31);
    return v__o32;
}

}  // namespace sfemul
