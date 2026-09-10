// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of shl_imm_gpr_32__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(28, 0, v0), 0)
@_cdecl("emu_shl_imm_gpr_32__reg_rdi__swift")
public func emu_shl_imm_gpr_32__reg_rdi__swift(_ a: UInt32) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(a))) &>> 0)) & UInt32(0x1fffffff)))) &<< 3) | (UInt64(truncatingIfNeeded: UInt32(0x0))))))
}
