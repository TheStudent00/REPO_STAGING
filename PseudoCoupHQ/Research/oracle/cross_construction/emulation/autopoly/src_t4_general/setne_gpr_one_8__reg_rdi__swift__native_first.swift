// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of setne_gpr_one_8__reg_rdi__swift__native_first.
//   Concat(Extract(63, 8, v0), If(Extract(7, 0, v1) == 0, 0, 1))
@_cdecl("emu_setne_gpr_one_8__reg_rdi__swift__native_first")
public func emu_setne_gpr_one_8__reg_rdi__swift__native_first(_ a: UInt8, _ b: UInt64) -> UInt64
{
    let v0: UInt32 = (UInt32(a))
    let v1: Bool = ((UInt32(truncatingIfNeeded: v0)) == (UInt32(truncatingIfNeeded: UInt32(0x0))))
    let v2: UInt32 = ((v1) ? (UInt32(0x0)) : (UInt32(0x1)))
    let v3: UInt64 = ((UInt64(truncatingIfNeeded: ((UInt64(b))) &>> 8)) & UInt64(0xffffffffffffff))
    let v4: UInt64 = (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: v3)) &<< 8) | (UInt64(truncatingIfNeeded: v2))))
    return UInt64(truncatingIfNeeded: v4)
}
