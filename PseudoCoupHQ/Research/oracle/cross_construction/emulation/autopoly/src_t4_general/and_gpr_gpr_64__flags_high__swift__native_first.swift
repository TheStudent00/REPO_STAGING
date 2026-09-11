// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of and_gpr_gpr_64__flags_high__swift__native_first.
//   ~(~v0 | ~v1)
@_cdecl("emu_and_gpr_gpr_64__flags_high__swift__native_first")
public func emu_and_gpr_gpr_64__flags_high__swift__native_first(_ a: UInt64, _ b: UInt64) -> UInt64
{
    let v0: UInt64 = (UInt64(truncatingIfNeeded: ~(UInt64(truncatingIfNeeded: (UInt64(b))))))
    let v1: UInt64 = (UInt64(truncatingIfNeeded: ~(UInt64(truncatingIfNeeded: (UInt64(a))))))
    let v2: UInt64 = (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: v1)) | (UInt64(truncatingIfNeeded: v0))))
    let v3: UInt64 = (UInt64(truncatingIfNeeded: ~(UInt64(truncatingIfNeeded: v2))))
    return UInt64(truncatingIfNeeded: v3)
}
