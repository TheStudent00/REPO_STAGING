// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of xor_imm_gpr_32__flags__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(31, 2, v0), ~Extract(1, 0, v0), 0)
@_cdecl("emu_xor_imm_gpr_32__flags__swift")
public func emu_xor_imm_gpr_32__flags__swift(_ a: UInt32) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(a))) &>> 2)) & UInt32(0x3fffffff)))) &<< 34) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ~(UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(a))) &>> 0)) & UInt32(0x3)))))) & UInt32(0x3)))) &<< 32) | (UInt64(truncatingIfNeeded: UInt32(0x0))))))
}
