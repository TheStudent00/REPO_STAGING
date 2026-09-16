#include "sfemul.h"


uint64_t ui32_to_f32_rm1(uint32_t v_arg)
{
    const bool v_i = (v_arg == UINT32_C(0x0));
    const bool v__n23 = (v_i != true);
    const uint32_t v__m24 = (uint32_t)((v__n23) ? ~(uint32_t)0 : (uint32_t)0);
    const bool v_i2 = ((int32_t)(v_arg) > INT32_C(-1));
    const uint32_t v__k1 = sf_ctlz32(v_arg);
    const uint32_t v_i10 = v__k1;
    const uint8_t v_i11 = (uint8_t)(v_i10);
    const uint8_t v_i12 = (uint8_t)(v_i11 + UINT32_C(0xff));
    const uint32_t v_i13 = (uint32_t)(v_i12);
    const uint16_t v_i14 = (uint16_t)(v_i12);
    const uint16_t v_i15 = (uint16_t)(UINT32_C(0x9c) - v_i14);
    const bool v_i16 = (v_arg < UINT32_C(0x1000000));
    const uint32_t v__sh3 = (uint32_t)((uint32_t)(v_arg) >> ((UINT32_C(0x8)) & 31));
    const uint32_t v_i8 = (uint32_t)(v__sh3 + UINT32_C(0x4e800000));
    const uint32_t v_i18 = (uint32_t)(v_i15);
    const uint32_t v__sh4 = (uint32_t)((uint32_t)(v_i18) << ((UINT32_C(0x17)) & 31));
    const uint32_t v_i19 = v__sh4;
    const uint32_t v_i20 = (uint32_t)(v_i13 + UINT32_C(0xfffffff9));
    const uint32_t v__sh5 = (uint32_t)((uint32_t)(v_arg) << ((v_i20) & 31));
    const uint32_t v_i21 = v__sh5;
    const uint32_t v_i22 = (uint32_t)(v_i21 + v_i19);
    const uint32_t v__sh6 = (uint32_t)((uint32_t)(v_arg) << ((v_i13) & 31));
    const uint32_t v_i23 = v__sh6;
    const uint32_t v__sh7 = (uint32_t)((uint32_t)(v_i23) >> ((UINT32_C(0x7)) & 31));
    const bool v_i27 = (v_i23 < UINT32_C(0x80));
    const uint32_t v__m9 = (uint32_t)((v_i27) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__n10 = (uint32_t)(v__m9 ^ UINT32_C(0xffffffff));
    const uint32_t v_i30 = (uint32_t)(v_i19 & v__n10);
    const uint32_t v_i31 = (uint32_t)(v__sh7 + v_i30);
    const bool v__n11 = (v_i2 != true);
    const uint32_t v__m12 = (uint32_t)((v__n11) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a13 = (uint32_t)(v_i8 & v__m12);
    const uint32_t v__m15 = (uint32_t)((v_i16) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a16 = (uint32_t)(v_i22 & v__m15);
    const uint32_t v__o17 = (uint32_t)(v__a13 | v__a16);
    const bool v__n18 = (v_i16 != true);
    const bool v__c19 = (v__n18 && v_i2);
    const uint32_t v__m20 = (uint32_t)((v__c19) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v__a21 = (uint32_t)(v_i31 & v__m20);
    const uint32_t v__o22 = (uint32_t)(v__o17 | v__a21);
    const uint32_t v__a25 = (uint32_t)(v__o22 & v__m24);
    const uint64_t v_i32 = (uint64_t)(v__a25);
    return v_i32;
}
