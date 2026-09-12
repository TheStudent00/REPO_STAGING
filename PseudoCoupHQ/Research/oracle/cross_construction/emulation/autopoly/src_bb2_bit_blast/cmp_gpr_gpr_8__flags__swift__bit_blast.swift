// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of cmp_gpr_gpr_8__flags__swift__bit_blast.
//   Concat(Extract(7, 0, v0), Extract(7, 0, v1))
@_cdecl("emu_cmp_gpr_gpr_8__flags__swift__bit_blast")
public func emu_cmp_gpr_gpr_8__flags__swift__bit_blast(_ a: UInt8, _ b: UInt8) -> UInt16
{
    let x1_0: UInt32 = (UInt32(truncatingIfNeeded: b) >> 0) & 1
    let x1_1: UInt32 = (UInt32(truncatingIfNeeded: b) >> 1) & 1
    let x1_2: UInt32 = (UInt32(truncatingIfNeeded: b) >> 2) & 1
    let x1_3: UInt32 = (UInt32(truncatingIfNeeded: b) >> 3) & 1
    let x1_4: UInt32 = (UInt32(truncatingIfNeeded: b) >> 4) & 1
    let x1_5: UInt32 = (UInt32(truncatingIfNeeded: b) >> 5) & 1
    let x1_6: UInt32 = (UInt32(truncatingIfNeeded: b) >> 6) & 1
    let x1_7: UInt32 = (UInt32(truncatingIfNeeded: b) >> 7) & 1
    let x0_0: UInt32 = (UInt32(truncatingIfNeeded: a) >> 0) & 1
    let x0_1: UInt32 = (UInt32(truncatingIfNeeded: a) >> 1) & 1
    let x0_2: UInt32 = (UInt32(truncatingIfNeeded: a) >> 2) & 1
    let x0_3: UInt32 = (UInt32(truncatingIfNeeded: a) >> 3) & 1
    let x0_4: UInt32 = (UInt32(truncatingIfNeeded: a) >> 4) & 1
    let x0_5: UInt32 = (UInt32(truncatingIfNeeded: a) >> 5) & 1
    let x0_6: UInt32 = (UInt32(truncatingIfNeeded: a) >> 6) & 1
    let x0_7: UInt32 = (UInt32(truncatingIfNeeded: a) >> 7) & 1
    let w0: UInt32 = (x1_0 << 0)
    let w1: UInt32 = w0 | (x1_1 << 1)
    let w2: UInt32 = w1 | (x1_2 << 2)
    let w3: UInt32 = w2 | (x1_3 << 3)
    let w4: UInt32 = w3 | (x1_4 << 4)
    let w5: UInt32 = w4 | (x1_5 << 5)
    let w6: UInt32 = w5 | (x1_6 << 6)
    let w7: UInt32 = w6 | (x1_7 << 7)
    let w8: UInt32 = w7 | (x0_0 << 8)
    let w9: UInt32 = w8 | (x0_1 << 9)
    let w10: UInt32 = w9 | (x0_2 << 10)
    let w11: UInt32 = w10 | (x0_3 << 11)
    let w12: UInt32 = w11 | (x0_4 << 12)
    let w13: UInt32 = w12 | (x0_5 << 13)
    let w14: UInt32 = w13 | (x0_6 << 14)
    let w15: UInt32 = w14 | (x0_7 << 15)
    return UInt16(truncatingIfNeeded: w15)
}
