// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of test_gpr_same_16__flags__swift__bit_blast.
//   Concat(Extract(15, 0, v0), 0)
@_cdecl("emu_test_gpr_same_16__flags__swift__bit_blast")
public func emu_test_gpr_same_16__flags__swift__bit_blast(_ a: UInt16) -> UInt32
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
    let k0: UInt32 = 0
    let w0: UInt32 = (k0 << 0)
    let w1: UInt32 = w0 | (k0 << 1)
    let w2: UInt32 = w1 | (k0 << 2)
    let w3: UInt32 = w2 | (k0 << 3)
    let w4: UInt32 = w3 | (k0 << 4)
    let w5: UInt32 = w4 | (k0 << 5)
    let w6: UInt32 = w5 | (k0 << 6)
    let w7: UInt32 = w6 | (k0 << 7)
    let w8: UInt32 = w7 | (k0 << 8)
    let w9: UInt32 = w8 | (k0 << 9)
    let w10: UInt32 = w9 | (k0 << 10)
    let w11: UInt32 = w10 | (k0 << 11)
    let w12: UInt32 = w11 | (k0 << 12)
    let w13: UInt32 = w12 | (k0 << 13)
    let w14: UInt32 = w13 | (k0 << 14)
    let w15: UInt32 = w14 | (k0 << 15)
    let w16: UInt32 = w15 | (x0_0 << 16)
    let w17: UInt32 = w16 | (x0_1 << 17)
    let w18: UInt32 = w17 | (x0_2 << 18)
    let w19: UInt32 = w18 | (x0_3 << 19)
    let w20: UInt32 = w19 | (x0_4 << 20)
    let w21: UInt32 = w20 | (x0_5 << 21)
    let w22: UInt32 = w21 | (x0_6 << 22)
    let w23: UInt32 = w22 | (x0_7 << 23)
    let w24: UInt32 = w23 | (x0_8 << 24)
    let w25: UInt32 = w24 | (x0_9 << 25)
    let w26: UInt32 = w25 | (x0_10 << 26)
    let w27: UInt32 = w26 | (x0_11 << 27)
    let w28: UInt32 = w27 | (x0_12 << 28)
    let w29: UInt32 = w28 | (x0_13 << 29)
    let w30: UInt32 = w29 | (x0_14 << 30)
    let w31: UInt32 = w30 | (x0_15 << 31)
    return UInt32(truncatingIfNeeded: w31)
}
