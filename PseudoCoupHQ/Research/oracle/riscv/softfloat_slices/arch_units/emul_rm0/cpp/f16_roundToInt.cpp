#include "sfemul.hpp"

namespace sfemul {


uint64_t f16_roundToInt_rm0(uint64_t v_arg, bool v_arg1)
{
    const uint16_t v_i = (uint16_t)(v_arg);
    const uint32_t v_i2 = (uint32_t)(v_arg);
    const uint32_t v_i3 = (uint32_t)(v_i2 & UINT32_C(0xffff));
    const uint32_t v_i4 = (uint32_t)((uint32_t)(v_i2) >> ((UINT32_C(0xa)) & 31));
    const uint32_t v_i5 = (uint32_t)(v_i4 & UINT32_C(0x1f));
    const bool v_i6 = (v_i5 < UINT32_C(0xf));
    const bool v_i18 = (v_i5 > UINT32_C(0x18));
    const uint64_t v_i8 = (uint64_t)(v_arg & UINT64_C(0x7fff));
    const bool v_i9 = (v_i8 == UINT64_C(0x0));
    const bool v_i20 = (v_i5 != UINT32_C(0x1f));
    const uint32_t v_i21 = (uint32_t)(v_i2 & UINT32_C(0x3ff));
    const bool v_i22 = (v_i21 == UINT32_C(0x0));
    const bool v_i23 = (v_i22 || v_i20);
    const uint16_t v__m1 = (uint16_t)((v_i23) ? ~(uint16_t)0 : (uint16_t)0);
    const bool v_i13 = (v_i21 != UINT32_C(0x0));
    const uint16_t v__a2 = (uint16_t)(v_i & v__m1);
    const uint16_t v__n3 = (uint16_t)(v__m1 ^ UINT32_C(0xffff));
    const uint16_t v__a4 = (uint16_t)(UINT32_C(0x7e00) & v__n3);
    const uint16_t v_spec_select4 = (uint16_t)(v__a2 | v__a4);
    const uint32_t v_i25 = (uint32_t)(UINT32_C(0x19) - v_i5);
    const bool v_i14 = (v_i5 == UINT32_C(0xe));
    const bool v_i15 = (v_i13 && v_i14);
    const uint16_t v__m12 = (uint16_t)((v_i15) ? ~(uint16_t)0 : (uint16_t)0);
    const uint32_t v__sh5 = (uint32_t)((uint32_t)(UINT32_C(0x1)) << ((v_i25) & 31));
    const uint32_t v_i26 = v__sh5;
    const uint32_t v__sh11 = (uint32_t)((uint32_t)(UINT32_C(0xffff)) << ((v_i25) & 31));
    const uint32_t v_i36 = v__sh11;
    const uint32_t v_i27 = (uint32_t)(v_i26 + UINT32_C(0xffff));
    const uint32_t v_i31 = (uint32_t)(v_i27 & UINT32_C(0xffff));
    const uint32_t v__sh6 = (uint32_t)((uint32_t)(v_i26) >> ((UINT32_C(0x1)) & 31));
    const uint32_t v_i29 = (uint32_t)(v__sh6 & UINT32_C(0x7fff));
    const uint32_t v_i30 = (uint32_t)(v_i29 + v_i3);
    const uint32_t v_i32 = (uint32_t)(v_i30 & v_i31);
    const bool v_i33 = (v_i32 == UINT32_C(0x0));
    const uint32_t v_i34 = (uint32_t)(v_i26 ^ UINT32_C(0xffffffff));
    const uint32_t v__m7 = (uint32_t)((v_i33) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a8 = (uint32_t)(v_i34 & v__m7);
    const uint32_t v__n9 = (uint32_t)(v__m7 ^ UINT32_C(0xffffffff));
    const uint32_t v__a10 = (uint32_t)(UINT32_C(0xfffe) & v__n9);
    const uint32_t v_i35 = (uint32_t)(v__a8 | v__a10);
    const uint32_t v_i37 = (uint32_t)(v_i35 & v_i36);
    const uint32_t v_i38 = (uint32_t)(v_i37 & v_i30);
    const uint16_t v_i39 = (uint16_t)(v_i38);
    const uint16_t v_i11 = (uint16_t)(v_i & UINT32_C(0x8000));
    const uint16_t v_i16 = (uint16_t)(v_i11 | UINT32_C(0x3c00));
    const uint16_t v__a13 = (uint16_t)(v_i16 & v__m12);
    const uint16_t v__n14 = (uint16_t)(v__m12 ^ UINT32_C(0xffff));
    const uint16_t v__a15 = (uint16_t)(v_i11 & v__n14);
    const uint16_t v_spec_select = (uint16_t)(v__a13 | v__a15);
    const bool v__c16 = (v_i9 && v_i6);
    const uint16_t v__m17 = (uint16_t)((v__c16) ? ~(uint16_t)0 : (uint16_t)0);
    const uint16_t v__a18 = (uint16_t)(v_i & v__m17);
    const bool v__n19 = (v_i9 != true);
    const bool v__c20 = (v__n19 && v_i6);
    const uint16_t v__m21 = (uint16_t)((v__c20) ? ~(uint16_t)0 : (uint16_t)0);
    const uint16_t v__a22 = (uint16_t)(v_spec_select & v__m21);
    const uint16_t v__o23 = (uint16_t)(v__a18 | v__a22);
    const bool v__n24 = (v_i6 != true);
    const bool v__n25 = (v_i18 != true);
    const bool v__c26 = (v__n24 && v__n25);
    const uint16_t v__m27 = (uint16_t)((v__c26) ? ~(uint16_t)0 : (uint16_t)0);
    const uint16_t v__a28 = (uint16_t)(v_i39 & v__m27);
    const uint16_t v__o29 = (uint16_t)(v__o23 | v__a28);
    const uint16_t v__m31 = (uint16_t)((v_i18) ? ~(uint16_t)0 : (uint16_t)0);
    const uint16_t v__a32 = (uint16_t)(v_spec_select4 & v__m31);
    const uint16_t v__o33 = (uint16_t)(v__o29 | v__a32);
    const uint64_t v_i41 = (uint64_t)(v__o33);
    return v_i41;
}

}  // namespace sfemul
