// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of seta_gpr_one_8__reg_rdi__swift__native_first.
//   Concat(Extract(63, 8, v1), If(And(Not(Extract(7, 0, v0) == 3), Or(Extract(1, 0, v0) == 3, Not(Extract(7, 2, v0) == 0))), 1, 0))
@_cdecl("emu_seta_gpr_one_8__reg_rdi__swift__native_first")
public func emu_seta_gpr_one_8__reg_rdi__swift__native_first(_ a: UInt8, _ b: UInt64) -> UInt64
{
    let v0: UInt32 = ((UInt32(truncatingIfNeeded: ((UInt32(a))) &>> 2)) & UInt32(0x3f))
    let v1: Bool = ((UInt32(truncatingIfNeeded: v0)) == (UInt32(truncatingIfNeeded: UInt32(0x0))))
    let v2: Bool = (!(v1))
    let v3: UInt32 = ((UInt32(truncatingIfNeeded: ((UInt32(a))) &>> 0)) & UInt32(0x3))
    let v4: Bool = ((UInt32(truncatingIfNeeded: v3)) == (UInt32(truncatingIfNeeded: UInt32(0x3))))
    let v5: Bool = ((v4) || (v2))
    let v6: UInt32 = (UInt32(a))
    let v7: Bool = ((UInt32(truncatingIfNeeded: v6)) == (UInt32(truncatingIfNeeded: UInt32(0x3))))
    let v8: Bool = (!(v7))
    let v9: Bool = ((v8) && (v5))
    let v10: UInt32 = ((v9) ? (UInt32(0x1)) : (UInt32(0x0)))
    let v11: UInt64 = ((UInt64(truncatingIfNeeded: ((UInt64(b))) &>> 8)) & UInt64(0xffffffffffffff))
    let v12: UInt64 = (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: v11)) &<< 8) | (UInt64(truncatingIfNeeded: v10))))
    return UInt64(truncatingIfNeeded: v12)
}
