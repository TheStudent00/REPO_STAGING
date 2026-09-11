// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of cmove_gpr_gpr_64__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   If(~(~Extract(63, 0, v0) | ~v1) == 0, v2, v3)
@_cdecl("emu_cmove_gpr_gpr_64__reg_rdi__swift")
public func emu_cmove_gpr_gpr_64__reg_rdi__swift(_ a: UInt64, _ b: UInt64, _ c: UInt64, _ d: UInt64) -> UInt64
{
    return UInt64(truncatingIfNeeded: ((((UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ~(UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ~(UInt64(truncatingIfNeeded: (UInt64(b)))))))) | (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ~(UInt64(truncatingIfNeeded: (UInt64(a)))))))))))))))) == (UInt64(truncatingIfNeeded: UInt64(0x0))))) ? ((UInt64(c))) : ((UInt64(d)))))
}
