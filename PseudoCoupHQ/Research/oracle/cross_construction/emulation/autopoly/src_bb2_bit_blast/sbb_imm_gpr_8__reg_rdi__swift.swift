// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of sbb_imm_gpr_8__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 8, v3), Extract(7, 0, v2)*255 + If(Extract(8, 8, Concat(0, Extract(7, 0, v0)) + Concat(0, Extract(7, 0, v1))) == 1, 1, 0)*255 + Extract(7, 0, v3))
@_cdecl("emu_sbb_imm_gpr_8__reg_rdi__swift")
public func emu_sbb_imm_gpr_8__reg_rdi__swift(_ a: UInt8, _ b: UInt8, _ c: UInt64, _ d: UInt8) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt64(c))) &>> 8)) & UInt64(0xffffffffffffff)))) &<< 8) | (UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: (UInt32(d)))) &* (UInt32(truncatingIfNeeded: UInt32(0xff))))) & UInt32(0xff)))) &+ (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: ((((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: UInt32(0x0))) &<< 8) | (UInt32(truncatingIfNeeded: (UInt32(b)))))) & UInt32(0x1ff)))) &+ (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: UInt32(0x0))) &<< 8) | (UInt32(truncatingIfNeeded: (UInt32(a)))))) & UInt32(0x1ff)))))) & UInt32(0x1ff)))) &>> 8)) & UInt32(0x1)))) == (UInt32(truncatingIfNeeded: UInt32(0x1))))) ? (UInt32(0x1)) : (UInt32(0x0))))) &* (UInt32(truncatingIfNeeded: UInt32(0xff))))) & UInt32(0xff)))) &+ (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt64(c))) &>> 0)) & UInt32(0xff)))))) & UInt32(0xff)))))))
}
