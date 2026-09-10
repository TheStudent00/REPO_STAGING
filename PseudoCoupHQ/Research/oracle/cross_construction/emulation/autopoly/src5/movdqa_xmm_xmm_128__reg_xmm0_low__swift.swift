// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of movdqa_xmm_xmm_128__reg_xmm0_low__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Extract(63, 0, v0)
@_cdecl("emu_movdqa_xmm_xmm_128__reg_xmm0_low__swift")
public func emu_movdqa_xmm_xmm_128__reg_xmm0_low__swift(_ a: Double) -> Double
{
    return Double(bitPattern: UInt64(truncatingIfNeeded: (UInt64((a).bitPattern))))
}
