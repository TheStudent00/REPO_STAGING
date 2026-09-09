// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of add_gpr_same_8__flags__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(7, 0, v0), Extract(7, 0, v0))
@_cdecl("emu_add_gpr_same_8__flags__swift")
public func emu_add_gpr_same_8__flags__swift(_ a: UInt8) -> UInt16
{
    return UInt16(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: (UInt32(a)))) &<< 8) | (UInt32(truncatingIfNeeded: (UInt32(a)))))) & UInt32(0xffff)))
}
