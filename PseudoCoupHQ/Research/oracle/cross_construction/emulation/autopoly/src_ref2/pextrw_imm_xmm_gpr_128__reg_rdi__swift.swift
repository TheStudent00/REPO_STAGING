// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of pextrw_imm_xmm_gpr_128__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 16, v0))
@_cdecl("emu_pextrw_imm_xmm_gpr_128__reg_rdi__swift")
public func emu_pextrw_imm_xmm_gpr_128__reg_rdi__swift(_ a: Float) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt64(0x0))) &<< 16) | (UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32((a).bitPattern))) &>> 16)) & UInt32(0xffff)))))))
}
