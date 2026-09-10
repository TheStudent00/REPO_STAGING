// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of cmpeqsd_xmm_xmm_64__reg_xmm0__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   If(And(fpEQ(fpToFP(Extract(63, 0, v0)), fpToFP(Extract(63, 0, v1))), Not(Or(fpIsNaN(fpToFP(Extract(63, 0, v0))), fpIsNaN(fpToFP(Extract(63, 0, v1)))))), 18446744073709551615, 0)
@_cdecl("emu_cmpeqsd_xmm_xmm_64__reg_xmm0__swift")
public func emu_cmpeqsd_xmm_xmm_64__reg_xmm0__swift(_ a: Double, _ b: Double) -> Double
{
    return Double(bitPattern: UInt64(truncatingIfNeeded: ((((((a) == (b))) && ((!(((((a) != (a))) || (((b) != (b))))))))) ? (UInt64(0xffffffffffffffff)) : (UInt64(0x0)))))
}
