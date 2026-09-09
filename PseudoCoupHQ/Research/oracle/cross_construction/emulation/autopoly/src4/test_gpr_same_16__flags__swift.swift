// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of test_gpr_same_16__flags__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(15, 0, v0), 0)
@_cdecl("emu_test_gpr_same_16__flags__swift")
public func emu_test_gpr_same_16__flags__swift(_ a: UInt16) -> UInt32
{
    return UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: (UInt32(a)))) &<< 16) | (UInt32(truncatingIfNeeded: UInt32(0x0))))))
}
