// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of neg_gpr_one_32__flags__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(31, 0, v0), 0)
@_cdecl("emu_neg_gpr_one_32__flags__swift")
public func emu_neg_gpr_one_32__flags__swift(_ a: UInt32) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: (UInt32(a)))) &<< 32) | (UInt64(truncatingIfNeeded: UInt32(0x0))))))
}
