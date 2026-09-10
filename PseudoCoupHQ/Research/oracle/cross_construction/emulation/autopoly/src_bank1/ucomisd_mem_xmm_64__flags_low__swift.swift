// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of ucomisd_mem_xmm_64__flags_low__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(v0))
@_cdecl("emu_ucomisd_mem_xmm_64__flags_low__swift")
public func emu_ucomisd_mem_xmm_64__flags_low__swift(_ a: UInt64) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64((Double(bitPattern: UInt64(truncatingIfNeeded: (UInt64(a))))).bitPattern)))
}
