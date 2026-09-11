// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of cmpeqsd_mem_xmm_64__reg_xmm0__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   If(And(fpEQ(fpToFP(Extract(63, 0, v0)), fpToFP(v1)), Not(Or(fpIsNaN(fpToFP(Extract(63, 0, v0))), fpIsNaN(fpToFP(v1))))), 18446744073709551615, 0)
@_cdecl("emu_cmpeqsd_mem_xmm_64__reg_xmm0__swift")
public func emu_cmpeqsd_mem_xmm_64__reg_xmm0__swift(_ a: UInt64, _ b: Double) -> Double
{
    return Double(bitPattern: UInt64(truncatingIfNeeded: ((((((b) == (Double(bitPattern: UInt64(truncatingIfNeeded: (UInt64(a))))))) && ((!(((((b) != (b))) || (((Double(bitPattern: UInt64(truncatingIfNeeded: (UInt64(a))))) != (Double(bitPattern: UInt64(truncatingIfNeeded: (UInt64(a))))))))))))) ? (UInt64(0xffffffffffffffff)) : (UInt64(0x0)))))
}
