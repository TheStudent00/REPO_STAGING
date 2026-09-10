// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of movq_xmm_gpr_64__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Extract(63, 0, v0)
@_cdecl("emu_movq_xmm_gpr_64__reg_rdi__swift")
public func emu_movq_xmm_gpr_64__reg_rdi__swift(_ a: Double) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64((a).bitPattern)))
}
