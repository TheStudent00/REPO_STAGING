// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of test_imm_gpr_8__flags__swift__bit_blast.
//   Concat(~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)), 0)
@_cdecl("emu_test_imm_gpr_8__flags__swift__bit_blast")
public func emu_test_imm_gpr_8__flags__swift__bit_blast(_ a: UInt8, _ b: UInt8) -> UInt16
{
    let x1_0: UInt32 = (UInt32(truncatingIfNeeded: a) >> 0) & 1
    let x0_0: UInt32 = (UInt32(truncatingIfNeeded: b) >> 0) & 1
    let x1_1: UInt32 = (UInt32(truncatingIfNeeded: a) >> 1) & 1
    let x0_1: UInt32 = (UInt32(truncatingIfNeeded: b) >> 1) & 1
    let x1_2: UInt32 = (UInt32(truncatingIfNeeded: a) >> 2) & 1
    let x0_2: UInt32 = (UInt32(truncatingIfNeeded: b) >> 2) & 1
    let x1_3: UInt32 = (UInt32(truncatingIfNeeded: a) >> 3) & 1
    let x0_3: UInt32 = (UInt32(truncatingIfNeeded: b) >> 3) & 1
    let x1_4: UInt32 = (UInt32(truncatingIfNeeded: a) >> 4) & 1
    let x0_4: UInt32 = (UInt32(truncatingIfNeeded: b) >> 4) & 1
    let x1_5: UInt32 = (UInt32(truncatingIfNeeded: a) >> 5) & 1
    let x0_5: UInt32 = (UInt32(truncatingIfNeeded: b) >> 5) & 1
    let x1_6: UInt32 = (UInt32(truncatingIfNeeded: a) >> 6) & 1
    let x0_6: UInt32 = (UInt32(truncatingIfNeeded: b) >> 6) & 1
    let x1_7: UInt32 = (UInt32(truncatingIfNeeded: a) >> 7) & 1
    let x0_7: UInt32 = (UInt32(truncatingIfNeeded: b) >> 7) & 1
    let k0: UInt32 = 0
    let g0: UInt32 = (x0_0 & x1_0)
    let g1: UInt32 = (x0_1 & x1_1)
    let g2: UInt32 = (x0_2 & x1_2)
    let g3: UInt32 = (x0_3 & x1_3)
    let g4: UInt32 = (x0_4 & x1_4)
    let g5: UInt32 = (x0_5 & x1_5)
    let g6: UInt32 = (x0_6 & x1_6)
    let g7: UInt32 = (x0_7 & x1_7)
    let w0: UInt32 = (k0 << 0)
    let w1: UInt32 = w0 | (k0 << 1)
    let w2: UInt32 = w1 | (k0 << 2)
    let w3: UInt32 = w2 | (k0 << 3)
    let w4: UInt32 = w3 | (k0 << 4)
    let w5: UInt32 = w4 | (k0 << 5)
    let w6: UInt32 = w5 | (k0 << 6)
    let w7: UInt32 = w6 | (k0 << 7)
    let w8: UInt32 = w7 | (g0 << 8)
    let w9: UInt32 = w8 | (g1 << 9)
    let w10: UInt32 = w9 | (g2 << 10)
    let w11: UInt32 = w10 | (g3 << 11)
    let w12: UInt32 = w11 | (g4 << 12)
    let w13: UInt32 = w12 | (g5 << 13)
    let w14: UInt32 = w13 | (g6 << 14)
    let w15: UInt32 = w14 | (g7 << 15)
    return UInt16(truncatingIfNeeded: w15)
}
