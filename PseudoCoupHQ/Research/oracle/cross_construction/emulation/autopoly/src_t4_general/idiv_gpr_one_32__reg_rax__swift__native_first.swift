// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of idiv_gpr_one_32__reg_rax__swift__native_first.
//   Concat(0, Extract(31, 0, bvsdiv_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2)))))
@_cdecl("emu_idiv_gpr_one_32__reg_rax__swift__native_first")
public func emu_idiv_gpr_one_32__reg_rax__swift__native_first(_ a: UInt32, _ b: UInt32, _ c: UInt32) -> UInt64
{
    let v0: UInt32 = (UInt32(c))
    let v1: UInt32 = ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1))
    let v2: UInt64 = (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: v1)) &<< 63) | ((UInt64(truncatingIfNeeded: v1)) &<< 62) | ((UInt64(truncatingIfNeeded: v1)) &<< 61) | ((UInt64(truncatingIfNeeded: v1)) &<< 60) | ((UInt64(truncatingIfNeeded: v1)) &<< 59) | ((UInt64(truncatingIfNeeded: v1)) &<< 58) | ((UInt64(truncatingIfNeeded: v1)) &<< 57) | ((UInt64(truncatingIfNeeded: v1)) &<< 56) | ((UInt64(truncatingIfNeeded: v1)) &<< 55) | ((UInt64(truncatingIfNeeded: v1)) &<< 54) | ((UInt64(truncatingIfNeeded: v1)) &<< 53) | ((UInt64(truncatingIfNeeded: v1)) &<< 52) | ((UInt64(truncatingIfNeeded: v1)) &<< 51) | ((UInt64(truncatingIfNeeded: v1)) &<< 50) | ((UInt64(truncatingIfNeeded: v1)) &<< 49) | ((UInt64(truncatingIfNeeded: v1)) &<< 48) | ((UInt64(truncatingIfNeeded: v1)) &<< 47) | ((UInt64(truncatingIfNeeded: v1)) &<< 46) | ((UInt64(truncatingIfNeeded: v1)) &<< 45) | ((UInt64(truncatingIfNeeded: v1)) &<< 44) | ((UInt64(truncatingIfNeeded: v1)) &<< 43) | ((UInt64(truncatingIfNeeded: v1)) &<< 42) | ((UInt64(truncatingIfNeeded: v1)) &<< 41) | ((UInt64(truncatingIfNeeded: v1)) &<< 40) | ((UInt64(truncatingIfNeeded: v1)) &<< 39) | ((UInt64(truncatingIfNeeded: v1)) &<< 38) | ((UInt64(truncatingIfNeeded: v1)) &<< 37) | ((UInt64(truncatingIfNeeded: v1)) &<< 36) | ((UInt64(truncatingIfNeeded: v1)) &<< 35) | ((UInt64(truncatingIfNeeded: v1)) &<< 34) | ((UInt64(truncatingIfNeeded: v1)) &<< 33) | ((UInt64(truncatingIfNeeded: v1)) &<< 32) | (UInt64(truncatingIfNeeded: v0))))
    let v3: UInt32 = (UInt32(b))
    let v4: UInt32 = (UInt32(a))
    let v5: UInt64 = (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: v4)) &<< 32) | (UInt64(truncatingIfNeeded: v3))))
    let v6: UInt64 = (UInt64(truncatingIfNeeded: UInt64(bitPattern: ((Int64(bitPattern: v5))) / ((Int64(bitPattern: v2))))))
    let v7: UInt32 = (UInt32(truncatingIfNeeded: (UInt64(truncatingIfNeeded: v6)) &>> 0))
    let v8: UInt64 = (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) | (UInt64(truncatingIfNeeded: v7))))
    return UInt64(truncatingIfNeeded: v8)
}
