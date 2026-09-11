// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of sete_gpr_one_8__reg_rdi__swift__all_constructed.
//   Concat(Extract(63, 8, v0), If(Extract(7, 0, v1) == 0, 1, 0))
@_cdecl("emu_sete_gpr_one_8__reg_rdi__swift__all_constructed")
public func emu_sete_gpr_one_8__reg_rdi__swift__all_constructed(_ a: UInt8, _ b: UInt64) -> UInt64
{
    let v0: UInt32 = (UInt32(a))
    let v1: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v0)) ^ (UInt32(truncatingIfNeeded: UInt32(0x0))))) & UInt32(0xff))
    let v2: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v1)) &>> (UInt32(truncatingIfNeeded: UInt32(0x1))))) & UInt32(0xff))
    let v3: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v1)) | (UInt32(truncatingIfNeeded: v2)))) & UInt32(0xff))
    let v4: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v3)) &>> (UInt32(truncatingIfNeeded: UInt32(0x2))))) & UInt32(0xff))
    let v5: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v3)) | (UInt32(truncatingIfNeeded: v4)))) & UInt32(0xff))
    let v6: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v5)) &>> (UInt32(truncatingIfNeeded: UInt32(0x4))))) & UInt32(0xff))
    let v7: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v5)) | (UInt32(truncatingIfNeeded: v6)))) & UInt32(0xff))
    let v8: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v7)) &>> 0)) & UInt32(0x1))
    let v9: Bool = ((UInt32(truncatingIfNeeded: UInt32(0x1))) == (UInt32(truncatingIfNeeded: v8)))
    let v10: Bool = (!(v9))
    let v11: UInt32 = ((v10) ? (UInt32(0x1)) : (UInt32(0x0)))
    let v12: UInt64 = ((UInt64(truncatingIfNeeded: ((UInt64(b))) &>> 8)) & UInt64(0xffffffffffffff))
    let v13: UInt32 = v11
    let v14: UInt64 = v12
    let v15: UInt64 = (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: v14)) &<< 8) | (UInt64(truncatingIfNeeded: v13))))
    return UInt64(truncatingIfNeeded: v15)
}
