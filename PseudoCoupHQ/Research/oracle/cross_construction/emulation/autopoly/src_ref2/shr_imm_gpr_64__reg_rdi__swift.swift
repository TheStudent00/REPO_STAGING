// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of shr_imm_gpr_64__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(63, 3, v0))
@_cdecl("emu_shr_imm_gpr_64__reg_rdi__swift")
public func emu_shr_imm_gpr_64__reg_rdi__swift(_ a: UInt64) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 61) | (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt64(a))) &>> 3)) & UInt64(0x1fffffffffffffff)))))))
}
