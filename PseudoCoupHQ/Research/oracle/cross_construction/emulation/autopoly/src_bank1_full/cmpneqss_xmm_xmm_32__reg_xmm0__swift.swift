// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of cmpneqss_xmm_xmm_32__reg_xmm0__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   If(And(fpEQ(fpToFP(Extract(31, 0, v0)), fpToFP(Extract(31, 0, v1))), Not(Or(fpIsNaN(fpToFP(Extract(31, 0, v0))), fpIsNaN(fpToFP(Extract(31, 0, v1)))))), 0, 4294967295)
@_cdecl("emu_cmpneqss_xmm_xmm_32__reg_xmm0__swift")
public func emu_cmpneqss_xmm_xmm_32__reg_xmm0__swift(_ a: Float, _ b: Float) -> Float
{
    return Float(bitPattern: UInt32(truncatingIfNeeded: ((((((a) == (b))) && ((!(((((a) != (a))) || (((b) != (b))))))))) ? (UInt32(0x0)) : (UInt32(0xffffffff)))))
}
