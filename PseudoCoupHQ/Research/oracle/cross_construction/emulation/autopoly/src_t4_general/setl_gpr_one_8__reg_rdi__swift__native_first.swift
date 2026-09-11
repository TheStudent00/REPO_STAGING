// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of setl_gpr_one_8__reg_rdi__swift__native_first.
//   Concat(Extract(63, 8, v1), If(Extract(7, 7, Extract(7, 0, v0) + 253) == If(Extract(7, 7, Concat(Extract(7, 7, v0), Extract(7, 0, v0)) + 509) == Extract(8, 8, Concat(Extract(7, 7, v0), Extract(7, 0, v0)) + 509), 1, 0), 1, 0))
@_cdecl("emu_setl_gpr_one_8__reg_rdi__swift__native_first")
public func emu_setl_gpr_one_8__reg_rdi__swift__native_first(_ a: UInt8, _ b: UInt64) -> UInt64
{
    let v0: UInt32 = (UInt32(a))
    let v1: UInt32 = ((UInt32(truncatingIfNeeded: ((UInt32(a))) &>> 7)) & UInt32(0x1))
    let v2: UInt32 = ((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: v1)) &<< 8) | (UInt32(truncatingIfNeeded: v0)))) & UInt32(0x1ff))
    let v3: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v2)) &+ (UInt32(truncatingIfNeeded: UInt32(0x1fd))))) & UInt32(0x1ff))
    let v4: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v3)) &>> 8)) & UInt32(0x1))
    let v5: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v3)) &>> 7)) & UInt32(0x1))
    let v6: Bool = ((UInt32(truncatingIfNeeded: v5)) == (UInt32(truncatingIfNeeded: v4)))
    let v7: UInt32 = ((v6) ? (UInt32(0x1)) : (UInt32(0x0)))
    let v8: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v0)) &+ (UInt32(truncatingIfNeeded: UInt32(0xfd))))) & UInt32(0xff))
    let v9: UInt32 = ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v8)) &>> 7)) & UInt32(0x1))
    let v10: Bool = ((UInt32(truncatingIfNeeded: v9)) == (UInt32(truncatingIfNeeded: v7)))
    let v11: UInt32 = ((v10) ? (UInt32(0x1)) : (UInt32(0x0)))
    let v12: UInt64 = ((UInt64(truncatingIfNeeded: ((UInt64(b))) &>> 8)) & UInt64(0xffffffffffffff))
    let v13: UInt64 = (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: v12)) &<< 8) | (UInt64(truncatingIfNeeded: v11))))
    return UInt64(truncatingIfNeeded: v13)
}
