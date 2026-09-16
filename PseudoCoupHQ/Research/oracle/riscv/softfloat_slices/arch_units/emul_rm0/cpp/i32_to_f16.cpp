#include "sfemul.hpp"

namespace sfemul {


uint64_t i32_to_f16_rm0(uint32_t v_arg)
{
    const bool v_i = ((int32_t)(v_arg) < INT32_C(0));
    const uint32_t v_i1 = sf_abs32(v_arg);
    const bool v_i2 = (v_arg == UINT32_C(0x0));
    const bool v__n15 = (v_i2 != true);
    const uint32_t v__k1 = sf_ctlz32(v_i1);
    const uint32_t v_i4 = v__k1;
    const bool v_i5 = (v_i1 < UINT32_C(0x800));
    const uint32_t v_i18 = (uint32_t)(v_i4 + UINT32_C(0xffffffef));
    const bool v_i19 = (v_i1 > UINT32_C(0x7fff));
    const uint32_t v_i7 = (uint32_t)(v_i4 + UINT32_C(0xeb));
    const uint32_t v_i10 = (uint32_t)(v_i7 & UINT32_C(0xff));
    const uint32_t v__sh2 = (uint32_t)((uint32_t)(v_arg) >> ((UINT32_C(0x10)) & 31));
    const uint32_t v_i9 = (uint32_t)(v__sh2 & UINT32_C(0x8000));
    const uint32_t v_i12 = (uint32_t)(v_i9 | UINT32_C(0x6000));
    const uint32_t v__sh3 = (uint32_t)((uint32_t)(v_i1) << ((v_i10) & 31));
    const uint32_t v_i11 = v__sh3;
    const uint32_t v__sh4 = (uint32_t)((uint32_t)(v_i10) << ((UINT32_C(0xa)) & 31));
    const uint32_t v_i14 = (uint32_t)(v_i12 - v__sh4);
    const uint32_t v_i15 = (uint32_t)(v_i14 + v_i11);
    const uint64_t v_i16 = (uint64_t)(v_i15);
    const uint32_t v_i21 = (uint32_t)(UINT32_C(0x11) - v_i4);
    const uint32_t v__sh5 = (uint32_t)((uint32_t)(v_i1) >> ((v_i21) & 31));
    const uint32_t v_i22 = v__sh5;
    const uint32_t v_i23 = (uint32_t)(v_i18 & UINT32_C(0x1f));
    const uint32_t v__sh6 = (uint32_t)((uint32_t)(v_i1) << ((v_i23) & 31));
    const uint32_t v_i24 = v__sh6;
    const bool v_i25 = (v_i24 != UINT32_C(0x0));
    const uint32_t v_i26 = (uint32_t)((v_i25) ? 1 : 0);
    const uint32_t v_i27 = (uint32_t)(v_i22 | v_i26);
    const uint32_t v__sh7 = (uint32_t)((uint32_t)(v_i1) << ((v_i18) & 31));
    const uint32_t v_i29 = v__sh7;
    const uint32_t v__m8 = (uint32_t)((v_i19) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a9 = (uint32_t)(v_i27 & v__m8);
    const bool v__n10 = (v_i19 != true);
    const uint32_t v__m11 = (uint32_t)((v__n10) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a12 = (uint32_t)(v_i29 & v__m11);
    const uint32_t v__o13 = (uint32_t)(v__a9 | v__a12);
    const bool v__n14 = (v_i5 != true);
    const bool v__c37 = (v_i5 && v__n15);
    const uint64_t v__m38 = (uint64_t)((v__c37) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a39 = (uint64_t)(v_i16 & v__m38);
    const bool v__c16 = (v__n14 && v__n15);
    const uint32_t v__m17 = (uint32_t)((v__c16) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a18 = (uint32_t)(v__o13 & v__m17);
    const uint32_t v_i32 = (uint32_t)(UINT32_C(0x2d) - v_i4);
    const bool v_i37 = (v_i4 != UINT32_C(0x10));
    const uint8_t v_i33 = (uint8_t)(v__a18);
    const uint8_t v_i43 = (uint8_t)(v_i33 & UINT32_C(0xf));
    const bool v_i48 = (v_i43 == UINT32_C(0x8));
    const uint32_t v_i49 = (uint32_t)((v_i48) ? 1 : 0);
    const uint32_t v_i50 = (uint32_t)(v_i49 ^ UINT32_C(0xffffffff));
    const uint32_t v_i36 = (uint32_t)(v__a18 & UINT32_C(0xfff8));
    const bool v_i38 = (v_i36 > UINT32_C(0x7ff7));
    const bool v_or_cond = (v_i37 || v_i38);
    const uint32_t v_i45 = (uint32_t)(v_i36 + UINT32_C(0x8));
    const uint32_t v__sh32 = (uint32_t)((uint32_t)(v_i45) >> ((UINT32_C(0x4)) & 31));
    const uint32_t v_i46 = v__sh32;
    const uint32_t v_i51 = (uint32_t)(v_i46 & v_i50);
    const uint64_t v__m19 = (uint64_t)((v_i) ? ~(uint64_t)0 : (uint64_t)0);
    const uint32_t v__m33 = (uint32_t)((v_i) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v_i53 = (uint32_t)(UINT32_C(0x8000) & v__m33);
    const uint32_t v_i56 = (uint32_t)(v_i51 | v_i53);
    const bool v_i52 = (v_i51 == UINT32_C(0x0));
    const uint32_t v__m35 = (uint32_t)((v_i52) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__n36 = (uint32_t)(v__m35 ^ UINT32_C(0xffffffff));
    const uint64_t v__a20 = (uint64_t)(UINT64_C(0xfc00) & v__m19);
    const uint64_t v__n21 = (uint64_t)(v__m19 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v__a22 = (uint64_t)(UINT64_C(0x7c00) & v__n21);
    const uint64_t v_i40 = (uint64_t)(v__a20 | v__a22);
    const uint32_t v__a25 = (uint32_t)(v_i32 & v__m11);
    const bool v__c40 = (v__n10 && v__n14);
    const bool v__c41 = (v__c40 && v__n15);
    const bool v__n26 = (v_or_cond != true);
    const bool v__c49 = (v_or_cond && v_i19);
    const bool v__c51 = (v__c49 && v__n15);
    const uint64_t v__m52 = (uint64_t)((v__c51) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a53 = (uint64_t)(v_i40 & v__m52);
    const bool v__c27 = (v__n26 && v_i19);
    const bool v__c44 = (v__c27 && v__n15);
    const bool v__c45 = (v__c41 || v__c44);
    const uint32_t v__m28 = (uint32_t)((v__c27) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a29 = (uint32_t)(UINT32_C(0x1d) & v__m28);
    const uint32_t v__o30 = (uint32_t)(v__a25 | v__a29);
    const uint32_t v__a31 = (uint32_t)(v__o30 & v__m17);
    const uint32_t v__sh34 = (uint32_t)((uint32_t)(v__a31) << ((UINT32_C(0xa)) & 31));
    const uint32_t v_i54 = v__sh34;
    const uint32_t v_i55 = (uint32_t)(v_i54 & v__n36);
    const uint32_t v_i57 = (uint32_t)(v_i56 + v_i55);
    const uint32_t v_i58 = (uint32_t)(v_i57 & UINT32_C(0xffff));
    const uint64_t v_i59 = (uint64_t)(v_i58);
    const uint64_t v__m46 = (uint64_t)((v__c45) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a47 = (uint64_t)(v_i59 & v__m46);
    const uint64_t v__o48 = (uint64_t)(v__a39 | v__a47);
    const uint64_t v__o54 = (uint64_t)(v__o48 | v__a53);
    const uint64_t v_i61 = (uint64_t)(v__o54 & UINT64_C(0xffff));
    return v_i61;
}

}  // namespace sfemul
