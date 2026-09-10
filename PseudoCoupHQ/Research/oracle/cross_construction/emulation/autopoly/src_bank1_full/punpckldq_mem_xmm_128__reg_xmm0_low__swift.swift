// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of punpckldq_mem_xmm_128__reg_xmm0_low__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(31, 0, v0), Extract(31, 0, v1))
@_cdecl("emu_punpckldq_mem_xmm_128__reg_xmm0_low__swift")
public func emu_punpckldq_mem_xmm_128__reg_xmm0_low__swift(_ a: UInt32, _ b: Float) -> Double
{
    return Double(bitPattern: UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: (UInt32(a)))) &<< 32) | (UInt64(truncatingIfNeeded: (UInt32((b).bitPattern))))))))
}
