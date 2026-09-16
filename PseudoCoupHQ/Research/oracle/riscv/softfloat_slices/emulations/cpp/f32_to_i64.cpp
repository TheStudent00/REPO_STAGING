#include "sfemul.hpp"

namespace sfemul {


uint64_t f32_to_i64_rm1(uint64_t v_arg)
{
    const uint32_t v_i = (uint32_t)(v_arg);
    const bool v_i1 = ((int32_t)(v_i) < INT32_C(0));
    const uint32_t v_i2 = (uint32_t)((uint32_t)(v_i) >> ((UINT32_C(0x17)) & 31));
    const uint32_t v_i4 = (uint32_t)(v_i2 & UINT32_C(0xff));
    const uint32_t v_i3 = (uint32_t)(v_i & UINT32_C(0x7fffff));
    const uint32_t v_i14 = (uint32_t)(v_i & UINT32_C(0x7f800000));
    const bool v_i15 = (v_i14 == UINT32_C(0x0));
    const uint32_t v__m1 = (uint32_t)((v_i15) ? ~(uint32_t)0 : (uint32_t)0);
    const uint32_t v_i5 = (uint32_t)(UINT32_C(0xbe) - v_i4);
    const bool v_i6 = (v_i4 > UINT32_C(0xbe));
    const uint32_t v_i16 = (uint32_t)(v_i3 | UINT32_C(0x800000));
    const uint32_t v__a2 = (uint32_t)(v_i3 & v__m1);
    const uint32_t v__n3 = (uint32_t)(v__m1 ^ UINT32_C(0xffffffff));
    const uint32_t v__a4 = (uint32_t)(v_i16 & v__n3);
    const uint32_t v_i17 = (uint32_t)(v__a2 | v__a4);
    const uint64_t v_i18 = (uint64_t)(v_i17);
    const uint64_t v__sh5 = (uint64_t)((uint64_t)(v_i18) << ((UINT64_C(0x28)) & 63));
    const uint64_t v_i19 = v__sh5;
    const bool v_i9 = (v_i3 != UINT32_C(0x0));
    const bool v_i20 = (v_i4 == UINT32_C(0xbe));
    const uint64_t v__m8 = (uint64_t)((v_i20) ? ~(uint64_t)0 : (uint64_t)0);
    const bool v_i8 = (v_i4 == UINT32_C(0xff));
    const bool v_i10 = (v_i9 && v_i8);
    const uint64_t v__m28 = (uint64_t)((v_i10) ? ~(uint64_t)0 : (uint64_t)0);
    const bool v_i21 = (v_i5 < UINT32_C(0x40));
    const uint64_t v_i22 = (uint64_t)(v_i5);
    const uint64_t v__sh6 = (uint64_t)((uint64_t)(v_i19) >> ((v_i22) & 63));
    const uint64_t v_i23 = v__sh6;
    const uint64_t v__m7 = (uint64_t)((v_i21) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v_i24 = (uint64_t)(v_i23 & v__m7);
    const uint64_t v__a9 = (uint64_t)(v_i19 & v__m8);
    const uint64_t v__n10 = (uint64_t)(v__m8 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v__a11 = (uint64_t)(v_i24 & v__n10);
    const uint64_t v_i25 = (uint64_t)(v__a9 | v__a11);
    const uint64_t v_i26 = (uint64_t)(UINT64_C(0x0) - v_i25);
    const uint64_t v__m12 = (uint64_t)((v_i1) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a13 = (uint64_t)(v_i26 & v__m12);
    const uint64_t v__n14 = (uint64_t)(v__m12 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v__a15 = (uint64_t)(v_i25 & v__n14);
    const uint64_t v_i27 = (uint64_t)(v__a13 | v__a15);
    const bool v_i28 = (v_i25 == UINT64_C(0x0));
    const bool v_i29 = ((int64_t)(v_i27) > INT64_C(-1));
    const bool v_i30 = (v_i1 != v_i29);
    const bool v_i31 = (v_i28 || v_i30);
    const uint64_t v__m20 = (uint64_t)((v_i31) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a21 = (uint64_t)(v_i27 & v__m20);
    const uint64_t v__n22 = (uint64_t)(v__m20 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v__a17 = (uint64_t)(UINT64_C(0x8000000000000000) & v__m12);
    const uint64_t v__a19 = (uint64_t)(UINT64_C(0x7fffffffffffffff) & v__n14);
    const uint64_t v_i32 = (uint64_t)(v__a17 | v__a19);
    const uint64_t v__a23 = (uint64_t)(v_i32 & v__n22);
    const uint64_t v_spec_select = (uint64_t)(v__a21 | v__a23);
    const uint64_t v__a29 = (uint64_t)(UINT64_C(0x7fffffffffffffff) & v__m28);
    const uint64_t v__n30 = (uint64_t)(v__m28 ^ UINT64_C(0xffffffffffffffff));
    const uint64_t v__a31 = (uint64_t)(v_i32 & v__n30);
    const uint64_t v_i12 = (uint64_t)(v__a29 | v__a31);
    const uint64_t v__m32 = (uint64_t)((v_i6) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a33 = (uint64_t)(v_i12 & v__m32);
    const bool v__n34 = (v_i6 != true);
    const uint64_t v__m35 = (uint64_t)((v__n34) ? ~(uint64_t)0 : (uint64_t)0);
    const uint64_t v__a36 = (uint64_t)(v_spec_select & v__m35);
    const uint64_t v__o37 = (uint64_t)(v__a33 | v__a36);
    return v__o37;
}

}  // namespace sfemul
