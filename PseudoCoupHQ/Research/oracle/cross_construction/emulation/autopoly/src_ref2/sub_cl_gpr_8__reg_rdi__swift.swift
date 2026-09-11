// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of sub_cl_gpr_8__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 8, v0), Extract(7, 0, v1)*255 + Extract(7, 0, v0))
@_cdecl("emu_sub_cl_gpr_8__reg_rdi__swift")
public func emu_sub_cl_gpr_8__reg_rdi__swift(_ a: UInt64, _ b: UInt8) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt64(a))) &>> 8)) & UInt64(0xffffffffffffff)))) &<< 8) | (UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: (UInt32(b)))) &* (UInt32(truncatingIfNeeded: UInt32(0xff))))) & UInt32(0xff)))) &+ (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt64(a))) &>> 0)) & UInt32(0xff)))))) & UInt32(0xff)))))))
}
