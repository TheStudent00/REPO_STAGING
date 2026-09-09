// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of or_imm_gpr_8__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(7, 2, v0), 3)
@_cdecl("emu_or_imm_gpr_8__reg_rdi__swift")
public func emu_or_imm_gpr_8__reg_rdi__swift(_ a: UInt8) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt64(0x0))) &<< 8) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(a))) &>> 2)) & UInt32(0x3f)))) &<< 2) | (UInt64(truncatingIfNeeded: UInt32(0x3))))))
}
