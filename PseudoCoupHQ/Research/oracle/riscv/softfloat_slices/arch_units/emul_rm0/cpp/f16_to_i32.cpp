#include "sfemul.hpp"

namespace sfemul {


uint32_t f16_to_i32_rm0(uint64_t v_arg)
{
    const uint64_t v_i = (uint64_t)(v_arg & UINT64_C(0x8000));
    const bool v_i1 = (v_i != UINT64_C(0x0));
    const uint64_t v_i2 = (uint64_t)((uint64_t)(v_arg) >> ((UINT64_C(0xa)) & 63));
    const uint8_t v_i3 = (uint8_t)(v_i2);
    const uint8_t v_i4 = (uint8_t)(v_i3 & UINT32_C(0x1f));
    const uint16_t v_i5 = (uint16_t)(v_arg);
    const uint16_t v_i6 = (uint16_t)(v_i5 & UINT32_C(0x3ff));
    const bool v_i7 = (v_i4 == UINT32_C(0x1f));
    const uint32_t v_i13 = (uint32_t)(v_i6);
    const bool v_i9 = (v_i6 == UINT32_C(0x0));
    const bool v_i10 = (v_i1 && v_i9);
    const uint32_t v__m1 = (uint32_t)((v_i10) ? ~(uint32_t)0 : (uint32_t)0);
    const bool v_i14 = (v_i4 == UINT32_C(0x0));
    const uint32_t v__a2 = (uint32_t)(UINT32_C(0x80000000) & v__m1);
    const uint32_t v__n3 = (uint32_t)(v__m1 ^ UINT32_C(0xffffffff));
    const uint32_t v__a4 = (uint32_t)(UINT32_C(0x7fffffff) & v__n3);
    const uint32_t v_i11 = (uint32_t)(v__a2 | v__a4);
    const uint32_t v_i16 = (uint32_t)(v_i13 | UINT32_C(0x400));
    const bool v_i17 = (v_i4 > UINT32_C(0x18));
    const uint8_t v_i19 = (uint8_t)(v_i4 + UINT32_C(0xe7));
    const uint32_t v_i20 = (uint32_t)(v_i19);
    const uint32_t v__sh5 = (uint32_t)((uint32_t)(v_i16) << ((v_i20) & 31));
    const uint32_t v_i21 = v__sh5;
    const uint32_t v_i22 = (uint32_t)(UINT32_C(0x0) - v_i21);
    const uint32_t v__m6 = (uint32_t)((v_i1) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a7 = (uint32_t)(v_i22 & v__m6);
    const uint32_t v__n8 = (uint32_t)(v__m6 ^ UINT32_C(0xffffffff));
    const uint32_t v__a9 = (uint32_t)(v_i21 & v__n8);
    const uint32_t v_i23 = (uint32_t)(v__a7 | v__a9);
    const bool v_i25 = (v_i4 > UINT32_C(0xd));
    const uint8_t v_i27 = (uint8_t)(v_i4 + UINT32_C(0xf3));
    const uint32_t v_i28 = (uint32_t)(v_i27);
    const uint32_t v__sh10 = (uint32_t)((uint32_t)(v_i16) << ((v_i28) & 31));
    const uint32_t v_i29 = v__sh10;
    const bool v__n11 = (v_i14 != true);
    const bool v__n12 = (v_i17 != true);
    const bool v__c13 = (v__n11 && v__n12);
    const bool v__c14 = (v__c13 && v_i25);
    const uint32_t v__m15 = (uint32_t)((v__c14) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a16 = (uint32_t)(v_i29 & v__m15);
    const bool v__n17 = (v_i25 != true);
    const bool v__c19 = (v__c13 && v__n17);
    const uint32_t v__m20 = (uint32_t)((v__c19) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a21 = (uint32_t)(v_i16 & v__m20);
    const uint32_t v__o22 = (uint32_t)(v__a16 | v__a21);
    const uint32_t v__m23 = (uint32_t)((v_i14) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a24 = (uint32_t)(v_i13 & v__m23);
    const uint32_t v__o25 = (uint32_t)(v__o22 | v__a24);
    const bool v__n26 = (v_i7 != true);
    const uint32_t v__m46 = (uint32_t)((v_i7) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a47 = (uint32_t)(v_i11 & v__m46);
    const uint32_t v__m27 = (uint32_t)((v__n26) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a28 = (uint32_t)(v__o25 & v__m27);
    const uint16_t v_i32 = (uint16_t)(v__a28);
    const uint16_t v_i33 = (uint16_t)(v_i32 & UINT32_C(0xfff));
    const uint32_t v_i34 = (uint32_t)(v__a28 + UINT32_C(0x800));
    const uint32_t v__sh29 = (uint32_t)((uint32_t)(v_i34) >> ((UINT32_C(0xc)) & 31));
    const uint32_t v_i35 = v__sh29;
    const bool v_i36 = (v_i33 == UINT32_C(0x800));
    const uint32_t v__m30 = (uint32_t)((v_i36) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v_i37 = (uint32_t)(v_i35 & UINT32_C(0xffffe));
    const uint32_t v__a31 = (uint32_t)(v_i37 & v__m30);
    const uint32_t v__n32 = (uint32_t)(v__m30 ^ UINT32_C(0xffffffff));
    const uint32_t v__a33 = (uint32_t)(v_i35 & v__n32);
    const uint32_t v_i38 = (uint32_t)(v__a31 | v__a33);
    const uint32_t v_i39 = (uint32_t)(UINT32_C(0x0) - v_i38);
    const uint32_t v__a35 = (uint32_t)(v_i39 & v__m6);
    const uint32_t v__a37 = (uint32_t)(v_i38 & v__n8);
    const uint32_t v_i40 = (uint32_t)(v__a35 | v__a37);
    const bool v_i41 = (v_i38 == UINT32_C(0x0));
    const bool v_i42 = ((int32_t)(v_i40) > INT32_C(-1));
    const bool v_i43 = (v_i1 != v_i42);
    const bool v_i44 = (v_i41 || v_i43);
    const uint32_t v__m42 = (uint32_t)((v_i44) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a43 = (uint32_t)(v_i40 & v__m42);
    const uint32_t v__n44 = (uint32_t)(v__m42 ^ UINT32_C(0xffffffff));
    const uint32_t v__a39 = (uint32_t)(UINT32_C(0x80000000) & v__m6);
    const uint32_t v__a41 = (uint32_t)(UINT32_C(0x7fffffff) & v__n8);
    const uint32_t v_i45 = (uint32_t)(v__a39 | v__a41);
    const uint32_t v__a45 = (uint32_t)(v_i45 & v__n44);
    const uint32_t v_spec_select = (uint32_t)(v__a43 | v__a45);
    const bool v__c48 = (v__n26 && v__n11);
    const bool v__c49 = (v__c48 && v_i17);
    const uint32_t v__m50 = (uint32_t)((v__c49) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a51 = (uint32_t)(v_i23 & v__m50);
    const uint32_t v__o52 = (uint32_t)(v__a47 | v__a51);
    const uint32_t v__m57 = (uint32_t)((v__n12) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a58 = (uint32_t)(v_spec_select & v__m57);
    const uint32_t v__o59 = (uint32_t)(v__o52 | v__a58);
    return v__o59;
}

}  // namespace sfemul
