// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of setg_gpr_one_8__reg_rdi__swift__all_constructed.
//   Concat(Extract(63, 8, v2), If(And(Not(~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)) == 0), Or(Extract(7, 7, v0) == 0, Extract(7, 7, v1) == 0)), 1, 0))
@_cdecl("emu_setg_gpr_one_8__reg_rdi__swift__all_constructed")
public func emu_setg_gpr_one_8__reg_rdi__swift__all_constructed(_ a: UInt8, _ b: UInt8, _ c: UInt64) -> UInt64
{
    let v0: UInt32 = ((UInt32(truncatingIfNeeded: ((UInt32(a))) &>> 7)) & UInt32(0x1))
    let v1: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v0)) ^ (UInt32(truncatingIfNeeded: UInt32(0x0))))) & UInt32(0x1))
    let v2: UInt32 = v1
    let v3: Bool = ((UInt32(truncatingIfNeeded: UInt32(0x1))) == (UInt32(truncatingIfNeeded: v2)))
    let v4: Bool = (!(v3))
    let v5: UInt32 = ((UInt32(truncatingIfNeeded: ((UInt32(b))) &>> 7)) & UInt32(0x1))
    let v6: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v5)) ^ (UInt32(truncatingIfNeeded: UInt32(0x0))))) & UInt32(0x1))
    let v7: UInt32 = v6
    let v8: Bool = ((UInt32(truncatingIfNeeded: UInt32(0x1))) == (UInt32(truncatingIfNeeded: v7)))
    let v9: Bool = (!(v8))
    let v10: Bool = ((v9) || (v4))
    let v11: UInt32 = (UInt32(a))
    let v12: UInt32 = ((UInt32(truncatingIfNeeded: ~(UInt32(truncatingIfNeeded: v11)))) & UInt32(0xff))
    let v13: UInt32 = (UInt32(b))
    let v14: UInt32 = ((UInt32(truncatingIfNeeded: ~(UInt32(truncatingIfNeeded: v13)))) & UInt32(0xff))
    let v15: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v14)) | (UInt32(truncatingIfNeeded: v12)))) & UInt32(0xff))
    let v16: UInt32 = ((UInt32(truncatingIfNeeded: ~(UInt32(truncatingIfNeeded: v15)))) & UInt32(0xff))
    let v17: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v16)) ^ (UInt32(truncatingIfNeeded: UInt32(0x0))))) & UInt32(0xff))
    let v18: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v17)) &>> (UInt32(truncatingIfNeeded: UInt32(0x1))))) & UInt32(0xff))
    let v19: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v17)) | (UInt32(truncatingIfNeeded: v18)))) & UInt32(0xff))
    let v20: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v19)) &>> (UInt32(truncatingIfNeeded: UInt32(0x2))))) & UInt32(0xff))
    let v21: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v19)) | (UInt32(truncatingIfNeeded: v20)))) & UInt32(0xff))
    let v22: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v21)) &>> (UInt32(truncatingIfNeeded: UInt32(0x4))))) & UInt32(0xff))
    let v23: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v21)) | (UInt32(truncatingIfNeeded: v22)))) & UInt32(0xff))
    let v24: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v23)) &>> 0)) & UInt32(0x1))
    let v25: Bool = ((UInt32(truncatingIfNeeded: UInt32(0x1))) == (UInt32(truncatingIfNeeded: v24)))
    let v26: Bool = (!(v25))
    let v27: Bool = (!(v26))
    let v28: Bool = ((v27) && (v10))
    let v29: UInt32 = ((v28) ? (UInt32(0x1)) : (UInt32(0x0)))
    let v30: UInt64 = ((UInt64(truncatingIfNeeded: ((UInt64(c))) &>> 8)) & UInt64(0xffffffffffffff))
    let v31: UInt32 = v29
    let v32: UInt64 = v30
    let v33: UInt64 = (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: v32)) &<< 8) | (UInt64(truncatingIfNeeded: v31))))
    return UInt64(truncatingIfNeeded: v33)
}
