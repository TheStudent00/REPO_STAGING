// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of setae_gpr_one_8__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 8, v0), If(ULE(Extract(7, 0, v1), Extract(7, 0, v2)), 1, 0))
@_cdecl("emu_setae_gpr_one_8__reg_rdi__swift")
public func emu_setae_gpr_one_8__reg_rdi__swift(_ a: UInt8, _ b: UInt8, _ c: UInt64) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt64(c))) &>> 8)) & UInt64(0xffffffffffffff)))) &<< 8) | (UInt64(truncatingIfNeeded: (((((UInt32(truncatingIfNeeded: (UInt32(b))))) <= ((UInt32(truncatingIfNeeded: (UInt32(a))))))) ? (UInt32(0x1)) : (UInt32(0x0))))))))
}
