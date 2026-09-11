// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of cmovs_gpr_gpr_64__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   If(Or(Extract(63, 63, v0) == 0, Extract(63, 63, v1) == 0), v2, v3)
@_cdecl("emu_cmovs_gpr_gpr_64__reg_rdi__swift")
public func emu_cmovs_gpr_gpr_64__reg_rdi__swift(_ a: UInt64, _ b: UInt64, _ c: UInt64, _ d: UInt64) -> UInt64
{
    return UInt64(truncatingIfNeeded: ((((((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt64(b))) &>> 63)) & UInt32(0x1)))) == (UInt32(truncatingIfNeeded: UInt32(0x0))))) || (((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt64(a))) &>> 63)) & UInt32(0x1)))) == (UInt32(truncatingIfNeeded: UInt32(0x0))))))) ? ((UInt64(d))) : ((UInt64(c)))))
}
