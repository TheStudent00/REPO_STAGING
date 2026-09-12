// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of neg_gpr_one_16__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 16, v0), Extract(15, 0, v0)*65535)
@_cdecl("emu_neg_gpr_one_16__reg_rdi__swift")
public func emu_neg_gpr_one_16__reg_rdi__swift(_ a: UInt64) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt64(a))) &>> 16)) & UInt64(0xffffffffffff)))) &<< 16) | (UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt64(a))) &>> 0)) & UInt32(0xffff)))) &* (UInt32(truncatingIfNeeded: UInt32(0xffff))))) & UInt32(0xffff)))))))
}
