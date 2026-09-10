// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of subsd_xmm_xmm_64__reg_xmm0__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(-fpToFP(Extract(63, 0, v0)) + fpToFP(Extract(63, 0, v1)))
@_cdecl("emu_subsd_xmm_xmm_64__reg_xmm0__swift")
public func emu_subsd_xmm_xmm_64__reg_xmm0__swift(_ a: Double, _ b: Double) -> Double
{
    return Double(bitPattern: UInt64(truncatingIfNeeded: (UInt64(((((-(a))) + (b))).bitPattern))))
}
