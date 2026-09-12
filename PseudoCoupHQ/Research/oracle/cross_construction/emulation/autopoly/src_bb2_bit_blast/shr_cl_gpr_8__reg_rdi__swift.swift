// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of shr_cl_gpr_8__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 8, v0), LShR(Extract(7, 0, v0), Concat(0, Extract(4, 0, v1))))
@_cdecl("emu_shr_cl_gpr_8__reg_rdi__swift")
public func emu_shr_cl_gpr_8__reg_rdi__swift(_ a: UInt64, _ b: UInt8) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt64(a))) &>> 8)) & UInt64(0xffffffffffffff)))) &<< 8) | (UInt64(truncatingIfNeeded: (((((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: UInt32(0x0))) &<< 5) | (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(b))) &>> 0)) & UInt32(0x1f)))))) & UInt32(0xff))))) < UInt32(0x8))) ? (((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt64(a))) &>> 0)) & UInt32(0xff)))) &>> (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: UInt32(0x0))) &<< 5) | (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(b))) &>> 0)) & UInt32(0x1f)))))) & UInt32(0xff)))))) & UInt32(0xff))) : (UInt32(0))))))))
}
