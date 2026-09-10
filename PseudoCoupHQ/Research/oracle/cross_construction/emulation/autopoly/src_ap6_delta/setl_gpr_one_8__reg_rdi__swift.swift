// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of setl_gpr_one_8__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(Extract(7, 0, v0) <= Extract(7, 0, v1), 0, 1))
@_cdecl("emu_setl_gpr_one_8__reg_rdi__swift")
public func emu_setl_gpr_one_8__reg_rdi__swift(_ a: UInt8, _ b: UInt8) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt64(0x0))) &<< 8) | (UInt64(truncatingIfNeeded: (((((((Int32(bitPattern: (UInt32(b)))) &<< 24) &>> 24)) <= ((((Int32(bitPattern: (UInt32(a)))) &<< 24) &>> 24)))) ? (UInt32(0x0)) : (UInt32(0x1))))))))
}
