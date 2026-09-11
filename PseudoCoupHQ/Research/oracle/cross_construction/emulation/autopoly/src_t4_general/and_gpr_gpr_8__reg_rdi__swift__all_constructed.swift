// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of and_gpr_gpr_8__reg_rdi__swift__all_constructed.
//   Concat(Extract(63, 8, v0), ~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)))
@_cdecl("emu_and_gpr_gpr_8__reg_rdi__swift__all_constructed")
public func emu_and_gpr_gpr_8__reg_rdi__swift__all_constructed(_ a: UInt64, _ b: UInt8) -> UInt64
{
    let v0: UInt32 = (UInt32(b))
    let v1: UInt32 = ((UInt32(truncatingIfNeeded: ~(UInt32(truncatingIfNeeded: v0)))) & UInt32(0xff))
    let v2: UInt32 = ((UInt32(truncatingIfNeeded: ((UInt64(a))) &>> 0)) & UInt32(0xff))
    let v3: UInt32 = ((UInt32(truncatingIfNeeded: ~(UInt32(truncatingIfNeeded: v2)))) & UInt32(0xff))
    let v4: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v3)) | (UInt32(truncatingIfNeeded: v1)))) & UInt32(0xff))
    let v5: UInt32 = ((UInt32(truncatingIfNeeded: ~(UInt32(truncatingIfNeeded: v4)))) & UInt32(0xff))
    let v6: UInt64 = ((UInt64(truncatingIfNeeded: ((UInt64(a))) &>> 8)) & UInt64(0xffffffffffffff))
    let v7: UInt32 = v5
    let v8: UInt64 = v6
    let v9: UInt64 = (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: v8)) &<< 8) | (UInt64(truncatingIfNeeded: v7))))
    return UInt64(truncatingIfNeeded: v9)
}
