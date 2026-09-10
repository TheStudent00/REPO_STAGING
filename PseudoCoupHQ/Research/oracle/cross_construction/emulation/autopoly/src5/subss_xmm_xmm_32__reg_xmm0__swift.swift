// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of subss_xmm_xmm_32__reg_xmm0__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(-fpToFP(Extract(31, 0, v0)) + fpToFP(Extract(31, 0, v1)))
@_cdecl("emu_subss_xmm_xmm_32__reg_xmm0__swift")
public func emu_subss_xmm_xmm_32__reg_xmm0__swift(_ a: Float, _ b: Float) -> Float
{
    return Float(bitPattern: UInt32(truncatingIfNeeded: (UInt32(((((-(b))) + (a))).bitPattern))))
}
