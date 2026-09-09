// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of cvtsi2sd_gpr_xmm_64__reg_xmm0__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(RNE(), v0))
@_cdecl("emu_cvtsi2sd_gpr_xmm_64__reg_xmm0__swift")
public func emu_cvtsi2sd_gpr_xmm_64__reg_xmm0__swift(_ a: UInt64) -> Double
{
    return Double(bitPattern: UInt64(truncatingIfNeeded: (UInt64((Double((Int64(bitPattern: (UInt64(a)))))).bitPattern))))
}
