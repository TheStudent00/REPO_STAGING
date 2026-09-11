// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of setg_gpr_one_8__reg_rdi__swift__native_first.
//   Concat(Extract(63, 8, v2), If(And(Not(~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)) == 0), Or(Extract(7, 7, v0) == 0, Extract(7, 7, v1) == 0)), 1, 0))
@_cdecl("emu_setg_gpr_one_8__reg_rdi__swift__native_first")
public func emu_setg_gpr_one_8__reg_rdi__swift__native_first(_ a: UInt8, _ b: UInt8, _ c: UInt64) -> UInt64
{
    let v0: UInt32 = ((UInt32(truncatingIfNeeded: ((UInt32(a))) &>> 7)) & UInt32(0x1))
    let v1: Bool = ((UInt32(truncatingIfNeeded: v0)) == (UInt32(truncatingIfNeeded: UInt32(0x0))))
    let v2: UInt32 = ((UInt32(truncatingIfNeeded: ((UInt32(b))) &>> 7)) & UInt32(0x1))
    let v3: Bool = ((UInt32(truncatingIfNeeded: v2)) == (UInt32(truncatingIfNeeded: UInt32(0x0))))
    let v4: Bool = ((v3) || (v1))
    let v5: UInt32 = (UInt32(a))
    let v6: UInt32 = ((UInt32(truncatingIfNeeded: ~(UInt32(truncatingIfNeeded: v5)))) & UInt32(0xff))
    let v7: UInt32 = (UInt32(b))
    let v8: UInt32 = ((UInt32(truncatingIfNeeded: ~(UInt32(truncatingIfNeeded: v7)))) & UInt32(0xff))
    let v9: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v8)) | (UInt32(truncatingIfNeeded: v6)))) & UInt32(0xff))
    let v10: UInt32 = ((UInt32(truncatingIfNeeded: ~(UInt32(truncatingIfNeeded: v9)))) & UInt32(0xff))
    let v11: Bool = ((UInt32(truncatingIfNeeded: v10)) == (UInt32(truncatingIfNeeded: UInt32(0x0))))
    let v12: Bool = (!(v11))
    let v13: Bool = ((v12) && (v4))
    let v14: UInt32 = ((v13) ? (UInt32(0x1)) : (UInt32(0x0)))
    let v15: UInt64 = ((UInt64(truncatingIfNeeded: ((UInt64(c))) &>> 8)) & UInt64(0xffffffffffffff))
    let v16: UInt64 = (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: v15)) &<< 8) | (UInt64(truncatingIfNeeded: v14))))
    return UInt64(truncatingIfNeeded: v16)
}
