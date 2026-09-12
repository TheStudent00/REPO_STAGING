// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of movd_gpr_xmm_32__reg_xmm0__swift__bit_blast.
//   Extract(31, 0, v0)
@_cdecl("emu_movd_gpr_xmm_32__reg_xmm0__swift__bit_blast")
public func emu_movd_gpr_xmm_32__reg_xmm0__swift__bit_blast(_ a: UInt32) -> Float
{
    let x0_0: UInt32 = (UInt32(truncatingIfNeeded: a) >> 0) & 1
    let x0_1: UInt32 = (UInt32(truncatingIfNeeded: a) >> 1) & 1
    let x0_2: UInt32 = (UInt32(truncatingIfNeeded: a) >> 2) & 1
    let x0_3: UInt32 = (UInt32(truncatingIfNeeded: a) >> 3) & 1
    let x0_4: UInt32 = (UInt32(truncatingIfNeeded: a) >> 4) & 1
    let x0_5: UInt32 = (UInt32(truncatingIfNeeded: a) >> 5) & 1
    let x0_6: UInt32 = (UInt32(truncatingIfNeeded: a) >> 6) & 1
    let x0_7: UInt32 = (UInt32(truncatingIfNeeded: a) >> 7) & 1
    let x0_8: UInt32 = (UInt32(truncatingIfNeeded: a) >> 8) & 1
    let x0_9: UInt32 = (UInt32(truncatingIfNeeded: a) >> 9) & 1
    let x0_10: UInt32 = (UInt32(truncatingIfNeeded: a) >> 10) & 1
    let x0_11: UInt32 = (UInt32(truncatingIfNeeded: a) >> 11) & 1
    let x0_12: UInt32 = (UInt32(truncatingIfNeeded: a) >> 12) & 1
    let x0_13: UInt32 = (UInt32(truncatingIfNeeded: a) >> 13) & 1
    let x0_14: UInt32 = (UInt32(truncatingIfNeeded: a) >> 14) & 1
    let x0_15: UInt32 = (UInt32(truncatingIfNeeded: a) >> 15) & 1
    let x0_16: UInt32 = (UInt32(truncatingIfNeeded: a) >> 16) & 1
    let x0_17: UInt32 = (UInt32(truncatingIfNeeded: a) >> 17) & 1
    let x0_18: UInt32 = (UInt32(truncatingIfNeeded: a) >> 18) & 1
    let x0_19: UInt32 = (UInt32(truncatingIfNeeded: a) >> 19) & 1
    let x0_20: UInt32 = (UInt32(truncatingIfNeeded: a) >> 20) & 1
    let x0_21: UInt32 = (UInt32(truncatingIfNeeded: a) >> 21) & 1
    let x0_22: UInt32 = (UInt32(truncatingIfNeeded: a) >> 22) & 1
    let x0_23: UInt32 = (UInt32(truncatingIfNeeded: a) >> 23) & 1
    let x0_24: UInt32 = (UInt32(truncatingIfNeeded: a) >> 24) & 1
    let x0_25: UInt32 = (UInt32(truncatingIfNeeded: a) >> 25) & 1
    let x0_26: UInt32 = (UInt32(truncatingIfNeeded: a) >> 26) & 1
    let x0_27: UInt32 = (UInt32(truncatingIfNeeded: a) >> 27) & 1
    let x0_28: UInt32 = (UInt32(truncatingIfNeeded: a) >> 28) & 1
    let x0_29: UInt32 = (UInt32(truncatingIfNeeded: a) >> 29) & 1
    let x0_30: UInt32 = (UInt32(truncatingIfNeeded: a) >> 30) & 1
    let x0_31: UInt32 = (UInt32(truncatingIfNeeded: a) >> 31) & 1
    let w0: UInt32 = (x0_0 << 0)
    let w1: UInt32 = w0 | (x0_1 << 1)
    let w2: UInt32 = w1 | (x0_2 << 2)
    let w3: UInt32 = w2 | (x0_3 << 3)
    let w4: UInt32 = w3 | (x0_4 << 4)
    let w5: UInt32 = w4 | (x0_5 << 5)
    let w6: UInt32 = w5 | (x0_6 << 6)
    let w7: UInt32 = w6 | (x0_7 << 7)
    let w8: UInt32 = w7 | (x0_8 << 8)
    let w9: UInt32 = w8 | (x0_9 << 9)
    let w10: UInt32 = w9 | (x0_10 << 10)
    let w11: UInt32 = w10 | (x0_11 << 11)
    let w12: UInt32 = w11 | (x0_12 << 12)
    let w13: UInt32 = w12 | (x0_13 << 13)
    let w14: UInt32 = w13 | (x0_14 << 14)
    let w15: UInt32 = w14 | (x0_15 << 15)
    let w16: UInt32 = w15 | (x0_16 << 16)
    let w17: UInt32 = w16 | (x0_17 << 17)
    let w18: UInt32 = w17 | (x0_18 << 18)
    let w19: UInt32 = w18 | (x0_19 << 19)
    let w20: UInt32 = w19 | (x0_20 << 20)
    let w21: UInt32 = w20 | (x0_21 << 21)
    let w22: UInt32 = w21 | (x0_22 << 22)
    let w23: UInt32 = w22 | (x0_23 << 23)
    let w24: UInt32 = w23 | (x0_24 << 24)
    let w25: UInt32 = w24 | (x0_25 << 25)
    let w26: UInt32 = w25 | (x0_26 << 26)
    let w27: UInt32 = w26 | (x0_27 << 27)
    let w28: UInt32 = w27 | (x0_28 << 28)
    let w29: UInt32 = w28 | (x0_29 << 29)
    let w30: UInt32 = w29 | (x0_30 << 30)
    let w31: UInt32 = w30 | (x0_31 << 31)
    return Float(bitPattern: UInt32(truncatingIfNeeded: w31))
}
