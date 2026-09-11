// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of or_gpr_gpr_32__flags__swift__native_first.
//   Concat(Extract(31, 0, v0) | Extract(31, 0, v1), 0)
@_cdecl("emu_or_gpr_gpr_32__flags__swift__native_first")
public func emu_or_gpr_gpr_32__flags__swift__native_first(_ a: UInt32, _ b: UInt32) -> UInt64
{
    let v0: UInt32 = (UInt32(b))
    let v1: UInt32 = (UInt32(a))
    let v2: UInt32 = (UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v1)) | (UInt32(truncatingIfNeeded: v0))))
    let v3: UInt64 = (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: v2)) &<< 32) | (UInt64(truncatingIfNeeded: UInt32(0x0)))))
    return UInt64(truncatingIfNeeded: v3)
}
