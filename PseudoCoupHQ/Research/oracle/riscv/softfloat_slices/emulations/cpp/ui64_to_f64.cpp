#include "sfemul.hpp"

namespace sfemul {


uint64_t ui64_to_f64_rm1(uint64_t v_arg)
{
    const bool v_i = (v_arg == UINT64_C(0x0));
    const bool v__n23 = (v_i != true);
    const uint64_t v__m24 = (uint64_t)((v__n23) ? ~(uint64_t)0 : (uint64_t)0);
    const bool v_i2 = ((int64_t)(v_arg) > INT64_C(-1));
    const uint64_t v__k1 = sf_ctlz64(v_arg);
    const uint64_t v_i10 = v__k1;
    const uint8_t v_i11 = (uint8_t)(v_i10);
    const uint8_t v_i12 = (uint8_t)(v_i11 + UINT32_C(0xff));
    const uint64_t v_i19 = (uint64_t)(v_i10 + UINT64_C(0xfffffff5));
    const uint64_t v_i20 = (uint64_t)(v_i19 & UINT64_C(0xffffffff));
    const uint64_t v__sh5 = (uint64_t)((uint64_t)(v_arg) << ((v_i20) & 63));
    const uint64_t v_i21 = v__sh5;
    const uint16_t v_i13 = (uint16_t)(v_i12);
    const uint16_t v_i14 = (uint16_t)(UINT32_C(0x43c) - v_i13);
    const uint64_t v_i23 = (uint64_t)(v_i12);
    const uint64_t v__sh6 = (uint64_t)((uint64_t)(v_arg) << ((v_i23) & 63));
    const uint64_t v_i24 = v__sh6;
    const bool v_i15 = (v_arg < UINT64_C(0x20000000000000));
    const uint64_t v__sh3 = (uint64_t)((uint64_t)(v_arg) >> ((UINT64_C(0xb)) & 63));
    const uint64_t v_i8 = (uint64_t)(v__sh3 + UINT64_C(0x43d0000000000000));
    const uint64_t v_i17 = (uint64_t)(v_i14);
    const uint64_t v__sh4 = (uint64_t)((uint64_t)(v_i17) << ((UINT64_C(0x34)) & 63));
    const uint64_t v_i18 = v__sh4;
    const uint64_t v_i22 = (uint64_t)(v_i21 + v_i18);
    const uint64_t v__sh7 = (uint64_t)((uint64_t)(v_i24) >> ((UINT64_C(0xa)) & 63));
    const bool v_i28 = (v_i24 < UINT64_C(0x400));
    const uint64_t v__m9 = (uint64_t)((v_i28) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__n10 = (uint64_t)(v__m9 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v_i31 = (uint64_t)(v_i18 & v__n10);
    const uint64_t v_i32 = (uint64_t)(v__sh7 + v_i31);
    const bool v__n11 = (v_i2 != true);
    const uint64_t v__m12 = (uint64_t)((v__n11) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a13 = (uint64_t)(v_i8 & v__m12);
    const uint64_t v__m15 = (uint64_t)((v_i15) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a16 = (uint64_t)(v_i22 & v__m15);
    const uint64_t v__o17 = (uint64_t)(v__a13 | v__a16);
    const bool v__n18 = (v_i15 != true);
    const bool v__c19 = (v__n18 && v_i2);
    const uint64_t v__m20 = (uint64_t)((v__c19) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a21 = (uint64_t)(v_i32 & v__m20);
    const uint64_t v__o22 = (uint64_t)(v__o17 | v__a21);
    const uint64_t v__a25 = (uint64_t)(v__o22 & v__m24);
    return v__a25;
}

}  // namespace sfemul
