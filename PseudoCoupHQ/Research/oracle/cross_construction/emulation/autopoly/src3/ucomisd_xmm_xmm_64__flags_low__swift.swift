// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of ucomisd_xmm_xmm_64__flags_low__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(Extract(63, 0, v0)))
@_cdecl("emu_ucomisd_xmm_xmm_64__flags_low__swift")
public func emu_ucomisd_xmm_xmm_64__flags_low__swift(_ a: Double) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64((a).bitPattern)))
}
