// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of sets_gpr_one_8__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 8, v2), If(Or(Extract(7, 7, v0) == 0, Extract(7, 7, v1) == 0), 0, 1))
@_cdecl("emu_sets_gpr_one_8__reg_rdi__swift")
public func emu_sets_gpr_one_8__reg_rdi__swift(_ a: UInt8, _ b: UInt8, _ c: UInt64) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt64(c))) &>> 8)) & UInt64(0xffffffffffffff)))) &<< 8) | (UInt64(truncatingIfNeeded: ((((((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(b))) &>> 7)) & UInt32(0x1)))) == (UInt32(truncatingIfNeeded: UInt32(0x0))))) || (((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(a))) &>> 7)) & UInt32(0x1)))) == (UInt32(truncatingIfNeeded: UInt32(0x0))))))) ? (UInt32(0x0)) : (UInt32(0x1))))))))
}
