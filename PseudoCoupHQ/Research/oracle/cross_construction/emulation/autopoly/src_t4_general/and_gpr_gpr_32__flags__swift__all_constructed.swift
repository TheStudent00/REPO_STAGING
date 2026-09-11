// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of and_gpr_gpr_32__flags__swift__all_constructed.
//   Concat(~(~Extract(31, 0, v0) | ~Extract(31, 0, v1)), 0)
@_cdecl("emu_and_gpr_gpr_32__flags__swift__all_constructed")
public func emu_and_gpr_gpr_32__flags__swift__all_constructed(_ a: UInt32, _ b: UInt32) -> UInt64
{
    let v0: UInt32 = (UInt32(b))
    let v1: UInt32 = (UInt32(truncatingIfNeeded: ~(UInt32(truncatingIfNeeded: v0))))
    let v2: UInt32 = (UInt32(a))
    let v3: UInt32 = (UInt32(truncatingIfNeeded: ~(UInt32(truncatingIfNeeded: v2))))
    let v4: UInt32 = (UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: v3)) | (UInt32(truncatingIfNeeded: v1))))
    let v5: UInt32 = (UInt32(truncatingIfNeeded: ~(UInt32(truncatingIfNeeded: v4))))
    let v6: UInt32 = UInt32(0x0)
    let v7: UInt32 = v5
    let v8: UInt64 = (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: v7)) &<< 32) | (UInt64(truncatingIfNeeded: v6))))
    return UInt64(truncatingIfNeeded: v8)
}
