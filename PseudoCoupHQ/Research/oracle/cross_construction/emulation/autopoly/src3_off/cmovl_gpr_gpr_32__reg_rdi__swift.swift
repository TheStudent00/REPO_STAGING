// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of cmovl_gpr_gpr_32__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(Extract(31, 0, v0) <= Extract(31, 0, v1), Extract(31, 0, v2), Extract(31, 0, v3)))
@_cdecl("emu_cmovl_gpr_gpr_32__reg_rdi__swift")
public func emu_cmovl_gpr_gpr_32__reg_rdi__swift(_ a: UInt32, _ b: UInt32, _ c: UInt32, _ d: UInt32) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) | (UInt64(truncatingIfNeeded: (((((Int32(bitPattern: (UInt32(b))))) <= ((Int32(bitPattern: (UInt32(a))))))) ? ((UInt32(d))) : ((UInt32(c)))))))))
}
