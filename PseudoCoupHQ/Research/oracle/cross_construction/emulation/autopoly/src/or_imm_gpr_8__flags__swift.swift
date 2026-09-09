// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of or_imm_gpr_8__flags__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(7, 2, v0), 768)
@_cdecl("emu_or_imm_gpr_8__flags__swift")
public func emu_or_imm_gpr_8__flags__swift(_ a: UInt8) -> UInt16
{
    return UInt16(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(a))) &>> 2)) & UInt32(0x3f)))) &<< 10) | (UInt32(truncatingIfNeeded: UInt32(0x300))))) & UInt32(0xffff)))
}
