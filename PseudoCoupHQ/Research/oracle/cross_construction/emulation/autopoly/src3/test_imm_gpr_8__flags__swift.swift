// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of test_imm_gpr_8__flags__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(1, 0, v0), 0)
@_cdecl("emu_test_imm_gpr_8__flags__swift")
public func emu_test_imm_gpr_8__flags__swift(_ a: UInt8) -> UInt16
{
    return UInt16(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: UInt32(0x0))) &<< 10) | ((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(a))) &>> 0)) & UInt32(0x3)))) &<< 8) | (UInt32(truncatingIfNeeded: UInt32(0x0))))) & UInt32(0xffff)))
}
