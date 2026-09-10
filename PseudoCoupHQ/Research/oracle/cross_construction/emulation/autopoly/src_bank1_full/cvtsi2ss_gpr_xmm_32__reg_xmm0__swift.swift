// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of cvtsi2ss_gpr_xmm_32__reg_xmm0__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(RNE(), Extract(31, 0, v0)))
@_cdecl("emu_cvtsi2ss_gpr_xmm_32__reg_xmm0__swift")
public func emu_cvtsi2ss_gpr_xmm_32__reg_xmm0__swift(_ a: UInt32) -> Float
{
    return Float(bitPattern: UInt32(truncatingIfNeeded: (UInt32((Float((Int32(bitPattern: (UInt32(a)))))).bitPattern))))
}
