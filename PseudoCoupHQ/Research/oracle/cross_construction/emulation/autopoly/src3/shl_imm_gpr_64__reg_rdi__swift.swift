// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of shl_imm_gpr_64__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(60, 0, v0), 0)
@_cdecl("emu_shl_imm_gpr_64__reg_rdi__swift")
public func emu_shl_imm_gpr_64__reg_rdi__swift(_ a: UInt64) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt64(a))) &>> 0)) & UInt64(0x1fffffffffffffff)))) &<< 3) | (UInt64(truncatingIfNeeded: UInt32(0x0))))))
}
