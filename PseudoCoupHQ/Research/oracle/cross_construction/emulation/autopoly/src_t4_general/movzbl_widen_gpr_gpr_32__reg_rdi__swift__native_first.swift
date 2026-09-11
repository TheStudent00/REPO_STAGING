// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of movzbl_widen_gpr_gpr_32__reg_rdi__swift__native_first.
//   Concat(0, Extract(7, 0, v0))
@_cdecl("emu_movzbl_widen_gpr_gpr_32__reg_rdi__swift__native_first")
public func emu_movzbl_widen_gpr_gpr_32__reg_rdi__swift__native_first(_ a: UInt8) -> UInt64
{
    let v0: UInt32 = (UInt32(a))
    let v1: UInt64 = (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt64(0x0))) &<< 8) | (UInt64(truncatingIfNeeded: v0))))
    return UInt64(truncatingIfNeeded: v1)
}
