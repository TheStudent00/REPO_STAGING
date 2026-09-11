// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of movd_gpr_xmm_32__reg_xmm0__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Extract(31, 0, v0)
@_cdecl("emu_movd_gpr_xmm_32__reg_xmm0__swift")
public func emu_movd_gpr_xmm_32__reg_xmm0__swift(_ a: UInt32) -> Float
{
    return Float(bitPattern: UInt32(truncatingIfNeeded: (UInt32(a))))
}
