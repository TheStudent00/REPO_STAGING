// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of movzbl_cl_gpr_32__reg_rdi__swift__all_constructed.
//   Concat(0, Extract(7, 0, v0))
@_cdecl("emu_movzbl_cl_gpr_32__reg_rdi__swift__all_constructed")
public func emu_movzbl_cl_gpr_32__reg_rdi__swift__all_constructed(_ a: UInt8) -> UInt64
{
    let v0: UInt32 = (UInt32(a))
    let v1: UInt32 = v0
    let v2: UInt64 = UInt64(0x0)
    let v3: UInt64 = (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: v2)) &<< 8) | (UInt64(truncatingIfNeeded: v1))))
    return UInt64(truncatingIfNeeded: v3)
}
